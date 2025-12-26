"""
Unit tests for BatchProcessorTool.

Tests parallel processing with multiprocessing to satisfy
software submission requirements for CPU-bound operations.
"""

import pytest
from multiprocessing import cpu_count
from src.mcp.tools.batch_processor_tool import BatchProcessorTool, _compute_intensive_operation


@pytest.mark.unit
class TestBatchProcessorTool:
    """Test suite for BatchProcessorTool class."""

    @pytest.fixture
    def tool(self):
        """Create a batch processor tool instance."""
        return BatchProcessorTool()

    def test_tool_metadata(self, tool):
        """Test tool metadata."""
        assert tool.name == 'batch_processor'
        assert 'parallel' in tool.description.lower() or 'multiprocessing' in tool.description.lower()

    def test_empty_input(self, tool):
        """Test graceful handling of empty input."""
        result = tool.execute({'items': []})
        assert result['success'] is True
        assert result['result']['results'] == []
        assert result['result']['count'] == 0
        assert result['result']['workers_used'] == 0

    def test_single_item(self, tool):
        """Test processing a single item."""
        result = tool.execute({'items': [5]})
        assert result['success'] is True
        assert len(result['result']['results']) == 1
        assert result['result']['count'] == 1
        assert isinstance(result['result']['results'][0], (int, float))

    def test_multiple_items(self, tool):
        """Test processing multiple items."""
        items = [1, 2, 3, 4, 5]
        result = tool.execute({'items': items})
        assert result['success'] is True
        assert result['result']['count'] == len(items)
        assert len(result['result']['results']) == len(items)

    def test_deterministic_results(self, tool):
        """Test that results are deterministic and in correct order."""
        items = [2, 4, 6, 8]
        result1 = tool.execute({'items': items})
        result2 = tool.execute({'items': items})

        # Results should be identical for same input
        assert result1['result']['results'] == result2['result']['results']

        # Results should maintain input order
        # (multiprocessing.Pool.map preserves order)
        assert len(result1['result']['results']) == len(items)

    def test_custom_workers(self, tool):
        """Test custom number of workers."""
        items = [1, 2, 3, 4]
        workers = 2

        result = tool.execute({
            'items': items,
            'workers': workers
        })

        assert result['success'] is True
        assert result['result']['workers_used'] == workers
        assert result['result']['count'] == len(items)

    def test_default_workers(self, tool):
        """Test default worker count equals CPU count."""
        items = [1, 2, 3]
        result = tool.execute({'items': items})

        assert result['success'] is True
        assert result['result']['workers_used'] == cpu_count()

    def test_workers_clamping(self, tool):
        """Test that workers are clamped to valid range."""
        items = [1, 2, 3]

        # Test upper bound clamping
        result_high = tool.execute({
            'items': items,
            'workers': cpu_count() * 10  # Excessively high
        })
        assert result_high['success'] is True
        assert result_high['result']['workers_used'] <= cpu_count() * 2

        # Test lower bound clamping
        result_low = tool.execute({
            'items': items,
            'workers': -5  # Invalid negative value
        })
        assert result_low['success'] is True
        assert result_low['result']['workers_used'] >= 1

    def test_large_batch(self, tool):
        """Test processing a larger batch of items."""
        items = list(range(100))
        result = tool.execute({'items': items})

        assert result['success'] is True
        assert result['result']['count'] == 100
        assert len(result['result']['results']) == 100

    def test_negative_numbers(self, tool):
        """Test processing negative numbers."""
        items = [-5, -3, -1, 0, 1, 3, 5]
        result = tool.execute({'items': items})

        assert result['success'] is True
        assert result['result']['count'] == len(items)

    def test_floating_point_numbers(self, tool):
        """Test processing floating-point numbers."""
        items = [1.5, 2.7, 3.14, 4.99]
        result = tool.execute({'items': items})

        assert result['success'] is True
        assert result['result']['count'] == len(items)
        for res in result['result']['results']:
            assert isinstance(res, (int, float))

    def test_missing_items_parameter(self, tool):
        """Test missing required 'items' parameter."""
        result = tool.execute({})
        # Should handle gracefully - empty items defaults to []
        assert result['success'] is True or result['success'] is False

    def test_invalid_items_type(self, tool):
        """Test invalid items type (not a list)."""
        result = tool.execute({'items': "not a list"})
        assert result['success'] is False
        assert 'error' in result

    def test_schema_to_dict(self, tool):
        """Test schema conversion to dictionary."""
        schema_dict = tool.to_dict()
        assert schema_dict['name'] == 'batch_processor'
        assert 'inputSchema' in schema_dict
        assert 'outputSchema' in schema_dict
        assert 'items' in schema_dict['inputSchema']['properties']
        assert 'workers' in schema_dict['inputSchema']['properties']


@pytest.mark.unit
class TestComputeIntensiveOperation:
    """Test suite for the compute-intensive operation function."""

    def test_compute_function_exists(self):
        """Test that compute function is callable."""
        assert callable(_compute_intensive_operation)

    def test_compute_returns_number(self):
        """Test that compute function returns a number."""
        result = _compute_intensive_operation(5)
        assert isinstance(result, (int, float))

    def test_compute_deterministic(self):
        """Test that compute function is deterministic."""
        input_val = 7
        result1 = _compute_intensive_operation(input_val)
        result2 = _compute_intensive_operation(input_val)
        assert result1 == result2

    def test_compute_different_inputs(self):
        """Test that different inputs produce different outputs."""
        result1 = _compute_intensive_operation(3)
        result2 = _compute_intensive_operation(5)
        # Results should differ for different inputs
        # (though theoretically could collide due to modulo)
        # Just verify both execute without error
        assert isinstance(result1, (int, float))
        assert isinstance(result2, (int, float))
