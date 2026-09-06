"""Shared setup: environment variables, the LLM, and the web search tool.

Everything here is created once and imported by the agent files.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch

# Load .env sitting next to this file
load_dotenv(Path(__file__).with_name(".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# One shared model for all agents
llm = init_chat_model(model="gpt-4o", model_provider="openai", temperature=0.2)

# One shared web search tool
internet_search = TavilySearch(
    max_results=5,
    topic="general",
    include_images=True,
    include_image_descriptions=True,
    search_depth="advanced",
)
