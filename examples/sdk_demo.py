#!/usr/bin/env python3
"""
SDK Demo - Shows how to use the MCP SDK programmatically.

This example demonstrates:
1. Creating an MCP client
2. Initializing the server
3. Listing available tools
4. Executing batch_processor (multiprocessing)
5. Executing concurrent_fetcher (multithreading)
"""

from src.sdk.mcp_client import MCPClient
from src.mcp.server import MCPServer
from src.mcp.tools.calculator_tool import CalculatorTool
from src.mcp.tools.echo_tool import EchoTool
from src.mcp.tools.batch_processor_tool import BatchProcessorTool
from src.mcp.tools.concurrent_fetcher_tool import ConcurrentFetcherTool
from src.mcp.resources.config_resource import ConfigResource
from src.mcp.resources.status_resource import StatusResource
from src.mcp.prompts.code_review_prompt import CodeReviewPrompt
from src.mcp.prompts.summarize_prompt import SummarizePrompt
import json


def main():
    """Run SDK demo."""
    print("=" * 60)
    print("MCP SDK Demo")
    print("=" * 60)
    print()

    # Step 1: Initialize MCP server
    print("1. Initializing MCP Server...")
    server = MCPServer()
    server.initialize(
        tools=[
            CalculatorTool(),
            EchoTool(),
            BatchProcessorTool(),
            ConcurrentFetcherTool()
        ],
        resources=[ConfigResource(), StatusResource()],
        prompts=[CodeReviewPrompt(), SummarizePrompt()]
    )
    print("   ✓ Server initialized")
    print()

    # Step 2: List available tools
    print("2. Listing Available Tools...")
    tools = server.get_tools_metadata()

    for tool in tools:
        print(f"   • {tool['name']}: {tool['description'][:60]}...")
    print()

    # Step 3: Execute batch_processor (multiprocessing)
    print("3. Executing batch_processor (Multiprocessing)...")
    response = server.execute_tool(
        'batch_processor',
        {'items': [1, 2, 3, 4, 5], 'workers': 2}
    )
    print(f"   Input: [1, 2, 3, 4, 5] with 2 workers")
    if response['success']:
        result = response['result']
        print(f"   Results: {len(result['results'])} items processed")
        print(f"   Workers used: {result['workers_used']}")
        print(f"   Sample result: {result['results'][0]:.2f}")
    print()

    # Step 4: Execute concurrent_fetcher (threading)
    print("4. Executing concurrent_fetcher (Multithreading)...")
    response = server.execute_tool(
        'concurrent_fetcher',
        {'items': ['apple', 'banana', 'cherry'], 'max_threads': 3}
    )
    print(f"   Input: ['apple', 'banana', 'cherry'] with 3 threads")
    if response['success']:
        result = response['result']
        print(f"   Results: {len(result['results'])} items processed")
        print(f"   Threads used: {result['threads_used']}")
        print(f"   Sample result: {result['results'][0]}")
    print()

    # Step 5: List resources
    print("5. Listing Available Resources...")
    resources = server.get_resources_metadata()

    for resource in resources:
        print(f"   • {resource['uri']}: {resource['description'][:50]}...")
    print()

    # Step 6: List prompts
    print("6. Listing Available Prompts...")
    prompts = server.get_prompts_metadata()

    for prompt in prompts:
        print(f"   • {prompt['name']}: {prompt['description'][:50]}...")
    print()

    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
