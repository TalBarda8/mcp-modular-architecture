"""
MCP Prompts package.
Contains base prompt abstraction and concrete prompt implementations.
"""

from src.mcp.prompts.base_prompt import BasePrompt
from src.mcp.prompts.code_review_prompt import CodeReviewPrompt
from src.mcp.prompts.summarize_prompt import SummarizePrompt

__all__ = ['BasePrompt', 'CodeReviewPrompt', 'SummarizePrompt']
