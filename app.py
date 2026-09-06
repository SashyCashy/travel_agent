"""Entry point. Pick an agent, ask it something, print the answer.

Layout:
  config.py                  -> env vars, shared LLM, shared web search tool
  tools.py                   -> flight + hotel search tools (SerpAPI)
  agents/itinerary_agent.py  -> day-by-day itinerary planner
  agents/search_agent.py     -> flight + hotel search agent
  agents/travel_scout.py     -> general travel Q&A (can call the itinerary agent)
"""

from agents.travel_scout import travel_scout


def ask(agent, question: str) -> str:
    """Send one question to an agent and return its final reply."""
    final_reply = None
    for event in agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
    ):
        messages = event.get("messages", [])
        if messages and messages[-1].content:
            final_reply = messages[-1].content

    if final_reply is None:
        raise RuntimeError("The agent stream produced no final reply.")
    return final_reply


if __name__ == "__main__":
    print(ask(travel_scout, "What is the best season to travel to Jodhpur?"))
