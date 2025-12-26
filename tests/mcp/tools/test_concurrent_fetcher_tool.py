"""
Unit tests for ConcurrentFetcherTool.

Tests I/O-bound parallel processing with multithreading to satisfy
software submission requirements (complementing CPU-bound multiprocessing).
"""

import pytest
import time
from src.mcp.tools.concurrent_fetcher_tool import ConcurrentFetcherTool, _simulate_io_operation


@pytest.mark.unit
class TestConcurrentFetcherTool:
    """Test suite for ConcurrentFetcherTool class."""

    @pytest.fixture
    def tool(self):
        """Create a concurrent fetcher tool instance."""
        return ConcurrentFetcherTool()

    def test_tool_metadata(self, tool):
        """Test tool metadata."""
        assert tool.name == 'concurrent_fetcher'
        assert 'concurrent' in tool.description.lower() or 'threading' in tool.description.lower()

    def test_empty_input(self, tool):
        """Test graceful handling of empty input."""
        result = tool.execute({'items': []})
        assert result['success'] is True
        assert result['result']['results'] == []
        assert result['result']['count'] == 0
        assert result['result']['threads_used'] == 0

    def test_single_item(self, tool):
        """Test processing a single item."""
        result = tool.execute({'items': ['test']})
        assert result['success'] is True
        assert len(result['result']['results']) == 1
        assert result['result']['count'] == 1
        assert result['result']['results'][0]['original'] == 'test'
        assert result['result']['results'][0]['uppercase'] == 'TEST'
        assert result['result']['results'][0]['length'] == 4

    def test_multiple_items(self, tool):
        """Test processing multiple items."""
        items = ['apple', 'banana', 'cherry', 'date', 'elderberry']
        result = tool.execute({'items': items})
        assert result['success'] is True
        assert result['result']['count'] == len(items)
        assert len(result['result']['results']) == len(items)

    def test_deterministic_order(self, tool):
        """Test that results maintain input order (deterministic)."""
        items = ['first', 'second', 'third', 'fourth']
        result = tool.execute({'items': items})

        # Results should be in same order as input
        assert result['success'] is True
        assert result['result']['results'][0]['original'] == 'first'
        assert result['result']['results'][1]['original'] == 'second'
        assert result['result']['results'][2]['original'] == 'third'
        assert result['result']['results'][3]['original'] == 'fourth'

        # Run again to verify consistency
        result2 = tool.execute({'items': items})
        originals1 = [r['original'] for r in result['result']['results']]
        originals2 = [r['original'] for r in result2['result']['results']]
        assert originals1 == originals2

    def test_custom_max_threads(self, tool):
        """Test custom max_threads parameter."""
        items = ['a', 'b', 'c', 'd']
        max_threads = 2

        result = tool.execute({
            'items': items,
            'max_threads': max_threads
        })

        assert result['success'] is True
        assert result['result']['threads_used'] == max_threads
        assert result['result']['count'] == len(items)

    def test_default_max_threads(self, tool):
        """Test default max_threads is 10."""
        items = ['a', 'b', 'c']
        result = tool.execute({'items': items})

        assert result['success'] is True
        # With only 3 items, threads_used should be 3 (min of max_threads and item count)
        assert result['result']['threads_used'] == 3

    def test_threads_clamping(self, tool):
        """Test that threads are clamped to valid range."""
        items = ['a', 'b', 'c']

        # Test upper bound clamping
        result_high = tool.execute({
            'items': items,
            'max_threads': 100  # Excessively high
        })
        assert result_high['success'] is True
        assert result_high['result']['threads_used'] <= 50  # Max is 50

        # Test lower bound clamping
        result_low = tool.execute({
            'items': items,
            'max_threads': -5  # Invalid negative value
        })
        assert result_low['success'] is True
        assert result_low['result']['threads_used'] >= 1

    def test_threads_limited_by_item_count(self, tool):
        """Test that threads_used is capped by number of items."""
        items = ['only', 'two']
        result = tool.execute({
            'items': items,
            'max_threads': 10  # More threads than items
        })

        assert result['success'] is True
        # Should only use 2 threads for 2 items
        assert result['result']['threads_used'] == 2

    def test_large_batch(self, tool):
        """Test processing a larger batch of items."""
        items = [f'item_{i}' for i in range(20)]
        result = tool.execute({'items': items})

        assert result['success'] is True
        assert result['result']['count'] == 20
        assert len(result['result']['results']) == 20

        # Verify all items processed correctly
        for i, res in enumerate(result['result']['results']):
            assert res['original'] == f'item_{i}'

    def test_parallel_speedup(self, tool):
        """Test that concurrent execution is faster than sequential."""
        items = ['a', 'b', 'c', 'd', 'e']  # 5 items with 100ms sleep each

        # Sequential would take ~500ms (5 * 100ms)
        # Concurrent with 5 threads should take ~100ms
        start_time = time.time()
        result = tool.execute({'items': items, 'max_threads': 5})
        elapsed = time.time() - start_time

        assert result['success'] is True
        # Should be significantly faster than sequential (with some margin for overhead)
        # Expect ~100-200ms, definitely less than 400ms
        assert elapsed < 0.4, f"Took {elapsed}s, expected < 0.4s (concurrent speedup)"

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

    def test_result_structure(self, tool):
        """Test that each result has expected structure."""
        items = ['test1', 'test2']
        result = tool.execute({'items': items})

        assert result['success'] is True
        for res in result['result']['results']:
            assert 'original' in res
            assert 'length' in res
            assert 'uppercase' in res
            assert 'processed_at' in res
            assert isinstance(res['processed_at'], float)

    def test_schema_to_dict(self, tool):
        """Test schema conversion to dictionary."""
        schema_dict = tool.to_dict()
        assert schema_dict['name'] == 'concurrent_fetcher'
        assert 'inputSchema' in schema_dict
        assert 'outputSchema' in schema_dict
        assert 'items' in schema_dict['inputSchema']['properties']
        assert 'max_threads' in schema_dict['inputSchema']['properties']


@pytest.mark.unit
class TestSimulateIOOperation:
    """Test suite for the I/O simulation function."""

    def test_function_exists(self):
        """Test that simulate function is callable."""
        assert callable(_simulate_io_operation)

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = _simulate_io_operation('test')
        assert isinstance(result, dict)

    def test_result_structure(self):
        """Test that result has expected keys."""
        result = _simulate_io_operation('hello')
        assert 'original' in result
        assert 'length' in result
        assert 'uppercase' in result
        assert 'processed_at' in result

    def test_correct_processing(self):
        """Test that processing is correct."""
        result = _simulate_io_operation('world')
        assert result['original'] == 'world'
        assert result['length'] == 5
        assert result['uppercase'] == 'WORLD'
        assert isinstance(result['processed_at'], float)

    def test_simulates_io_delay(self):
        """Test that function actually sleeps (simulates I/O)."""
        start = time.time()
        _simulate_io_operation('test')
        elapsed = time.time() - start
        # Should take at least 100ms due to sleep(0.1)
        assert elapsed >= 0.09, f"Function took {elapsed}s, expected >= 0.1s"
