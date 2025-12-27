"""
Batch Processor Tool - Demonstrates CPU-bound parallel processing using multiprocessing.

This tool showcases multiprocessing for computationally intensive tasks, satisfying
the parallel processing requirements outlined in software submission guidelines.
"""

from typing import Any, Dict, List
from multiprocessing import Pool, cpu_count

from src.mcp.tools.base_tool import BaseTool
from src.mcp.schemas.tool_schemas import ToolSchema
from src.core.errors.exceptions import ValidationError


def _compute_intensive_operation(number: float) -> float:
    """
    Simulate a CPU-intensive operation.

    This function is defined at module level (not as a class method) because
    multiprocessing.Pool requires picklable functions, and class methods
    can cause serialization issues.

    Args:
        number: Input number to process

    Returns:
        Processed result (number squared plus some computation)
    """
    # Simulate CPU-intensive work
    result = number ** 2
    # Add some additional computation to make it more CPU-intensive
    for i in range(1000):
        result = (result + i * 0.0001) % 1000000
    return result


class BatchProcessorTool(BaseTool):
    """
    Batch processor for CPU-bound parallel processing using multiprocessing.

    Uses multiprocessing.Pool (not threading) to bypass Python's GIL and achieve
    true parallelism for CPU-intensive computations across multiple cores.
    """

    def _define_schema(self) -> ToolSchema:
        """Define the batch processor tool schema."""
        return ToolSchema(
            name='batch_processor',
            description='Process a batch of numbers in parallel using multiprocessing (CPU-bound)',
            input_schema={
                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': {'type': 'number'},
                        'description': 'List of numbers to process in parallel',
                        'minItems': 0
                    },
                    'workers': {
                        'type': 'integer',
                        'description': f'Number of worker processes (default: {cpu_count()})',
                        'minimum': 1,
                        'maximum': cpu_count() * 2,
                        'default': cpu_count()
                    }
                },
                'required': ['items']
            },
            output_schema={
                'type': 'object',
                'properties': {
                    'results': {
                        'type': 'array',
                        'items': {'type': 'number'},
                        'description': 'Processed results'
                    },
                    'count': {
                        'type': 'integer',
                        'description': 'Number of items processed'
                    },
                    'workers_used': {
                        'type': 'integer',
                        'description': 'Number of worker processes used'
                    }
                }
            }
        )

    def _execute_impl(self, params: Dict[str, Any]) -> Any:
        """Execute CPU-intensive batch processing with multiprocessing."""
        items = params.get('items', [])
        workers = params.get('workers', cpu_count())

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
                'workers_used': 0
            }

        # Ensure workers is within valid range
        workers = max(1, min(workers, cpu_count() * 2))

        self.logger.info(
            f"Processing {len(items)} items using {workers} worker processes"
        )

        # Use multiprocessing.Pool for parallel CPU-bound processing
        # Pool automatically manages process lifecycle
        with Pool(processes=workers) as pool:
            # pool.map distributes work across processes
            # Returns results in the same order as input
            results = pool.map(_compute_intensive_operation, items)

        self.logger.info(f"Batch processing completed: {len(results)} items processed")

        return {
            'results': results,
            'count': len(results),
            'workers_used': workers
        }
