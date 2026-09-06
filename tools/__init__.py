"""Tools the agents can call.

Re-exported here so agents can just do:
    from tools import search_flights, search_hotels
"""

from tools.flights import search_flights
from tools.hotels import search_hotels

__all__ = ["search_flights", "search_hotels"]
