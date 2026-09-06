"""Itinerary agent: researches destinations and builds day-by-day plans."""

from deepagents import create_deep_agent

from config import llm, internet_search
from prompts.itinerary_agent import research_instructions

itinerary_research_agent = create_deep_agent(
    model=llm,
    system_prompt=research_instructions,
    tools=[internet_search],
)
