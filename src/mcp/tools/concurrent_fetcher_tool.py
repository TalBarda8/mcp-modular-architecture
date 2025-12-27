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

    Uses threading (not multiprocessing) because I/O-bound tasks spend most time
    waiting for external operations. Python releases the GIL during I/O, allowing
    threads to run concurrently with much lower overhead than processes.

    Thread-safe: no shared mutable state, results collected by ThreadPoolExecutor.map().
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
        """Execute concurrent I/O processing with threading."""
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
