"""
Concurrent Fetcher Tool - Demonstrates I/O-bound parallelism using multithreading.

This tool showcases threading for I/O-bound tasks, complementing the CPU-bound
multiprocessing example. Together they satisfy the parallel processing requirements
outlined in software submission guidelines.
"""

from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor
import time

from src.mcp.tools.base_tool import BaseTool
from src.mcp.schemas.tool_schemas import ToolSchema
from src.core.errors.exceptions import ValidationError


def _simulate_io_operation(item: str) -> Dict[str, Any]:
    """
    Simulate an I/O-bound operation (e.g., network request, file read, database query).

    This function is defined at module level for clarity, though unlike multiprocessing,
    threading doesn't require picklable functions.

    Args:
        item: Input string to process

    Returns:
        Dictionary with processed result and metadata
    """
    # Simulate I/O wait time (e.g., network latency, disk I/O)
    # During time.sleep(), Python releases the GIL, allowing other threads to run
    time.sleep(0.1)  # 100ms simulated I/O latency

    # Simulate some lightweight processing after I/O
    result = {
        'original': item,
        'length': len(item),
        'uppercase': item.upper(),
        'processed_at': time.time()
    }

    return result


class ConcurrentFetcherTool(BaseTool):
    """
    Concurrent fetcher for I/O-bound parallelism using multithreading.

    **Why Threading (not Multiprocessing)?**

    This tool demonstrates I/O-bound parallel processing, which is fundamentally
    different from CPU-bound processing:

    - **I/O-bound tasks**: Spend most time waiting for external operations
      (network requests, file I/O, database queries)
      → Use threading because:
        1. Python releases the GIL during I/O operations
        2. Threads can run concurrently while waiting for I/O
        3. Much lower overhead than processes (shared memory space)
        4. No serialization/pickling needed

    - **CPU-bound tasks**: Spend most time doing computation
      → Use multiprocessing (see BatchProcessorTool)
        1. Multiprocessing bypasses GIL for true parallelism
        2. Each process has its own Python interpreter

    **Why Multiprocessing Would Be Inefficient Here:**

    1. **Process overhead**: Creating processes is expensive (~10-100ms each)
       vs threads (~1ms). For I/O tasks that already wait, this overhead dominates.

    2. **Memory**: Each process duplicates memory, threads share it.
       For I/O tasks that don't need isolation, this is wasteful.

    3. **IPC cost**: Processes need serialization (pickle) for communication.
       Threads share memory directly.

    4. **Context switching**: OS switches between threads faster than processes.

    **Thread Safety:**

    This implementation is thread-safe without locks because:
    - No shared mutable state between threads
    - No global variables modified during execution
    - Each thread processes independent data
    - Results are collected by ThreadPoolExecutor.map() which handles synchronization
    - Input order is preserved automatically by .map()

    **Use Case:**
    Process a list of items with I/O-bound operations (simulated network fetches,
    file reads, API calls) concurrently, achieving significant speedup without
    the overhead of multiprocessing.

    **Architecture Note:**
    Like BatchProcessorTool, this follows MCP's extensibility principle - it's
    a standalone module that registers via ToolRegistry without modifying core
    server code.
    """

    def _define_schema(self) -> ToolSchema:
        """Define the concurrent fetcher tool schema."""
        return ToolSchema(
            name='concurrent_fetcher',
            description='Process items concurrently using multithreading (I/O-bound)',
            input_schema={
                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'List of items to process concurrently',
                        'minItems': 0
                    },
                    'max_threads': {
                        'type': 'integer',
                        'description': 'Maximum number of worker threads (default: 10)',
                        'minimum': 1,
                        'maximum': 50,
                        'default': 10
                    }
                },
                'required': ['items']
            },
            output_schema={
                'type': 'object',
                'properties': {
                    'results': {
                        'type': 'array',
                        'items': {'type': 'object'},
                        'description': 'Processed results in original order'
                    },
                    'count': {
                        'type': 'integer',
                        'description': 'Number of items processed'
                    },
                    'threads_used': {
                        'type': 'integer',
                        'description': 'Number of worker threads used'
                    }
                }
            }
        )

    def _execute_impl(self, params: Dict[str, Any]) -> Any:
        """
        Execute concurrent processing with threading.

        Args:
            params: Must contain 'items' (list of strings),
                   optional 'max_threads' (int)

        Returns:
            Dictionary with processed results, count, and threads used

        Raises:
            ValidationError: If items list is invalid
        """
        items = params.get('items', [])
        max_threads = params.get('max_threads', 10)

        # Validate items
        if not isinstance(items, list):
            raise ValidationError(
                "Items must be a list",
                {'items_type': type(items).__name__}
            )

        # Handle empty input gracefully
        if not items:
            self.logger.info("Empty items list provided, returning empty results")
            return {
                'results': [],
                'count': 0,
                'threads_used': 0
            }

        # Ensure max_threads is within valid range
        max_threads = max(1, min(max_threads, 50))

        # Actual threads used is min of max_threads and number of items
        # (no point using more threads than items)
        threads_used = min(max_threads, len(items))

        self.logger.info(
            f"Processing {len(items)} items using {threads_used} worker threads"
        )

        # Use ThreadPoolExecutor for parallel I/O-bound processing
        # Context manager automatically manages thread lifecycle
        with ThreadPoolExecutor(max_workers=threads_used) as executor:
            # executor.map distributes work across threads
            # Returns results in the same order as input (deterministic)
            # GIL is released during I/O operations (time.sleep), allowing parallelism
            results = list(executor.map(_simulate_io_operation, items))

        self.logger.info(f"Concurrent processing completed: {len(results)} items processed")

        return {
            'results': results,
            'count': len(results),
            'threads_used': threads_used
        }
