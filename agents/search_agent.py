"""Search agent: finds flights and hotels using the SerpAPI tools."""

from langchain.agents import create_agent

from config import llm
from tools import search_flights, search_hotels
from prompts.search_agent import flightHotelSearch_instructions

search_agent = create_agent(
    model=llm,
    system_prompt=flightHotelSearch_instructions,
    tools=[search_flights, search_hotels],
)
