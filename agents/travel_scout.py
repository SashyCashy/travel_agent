"""Travel scout: answers general travel questions.

It can hand off deep, day-by-day planning to the itinerary agent, which is
wrapped as a tool below.
"""

from langchain_core.tools import tool
from langchain.agents import create_agent

from config import llm, internet_search
from agents.itinerary_agent import itinerary_research_agent
from prompts.travel_scout import travel_scout_instructions

# Wrap the itinerary agent so the scout can call it like any other tool.
@tool("itinerary_research_agent", description="plans travel itinerary")
def call_itinerary_research_agent(query: str):
    result = itinerary_research_agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    return result["messages"][-1].content


travel_scout = create_agent(
    model=llm,
    system_prompt=travel_scout_instructions,
    tools=[internet_search, call_itinerary_research_agent],
)
