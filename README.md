# Travel Agent

A small multi-agent travel assistant built with LangChain / `deepagents`. One
top-level agent answers general travel questions and delegates to two
specialist agents for deep itinerary planning and for flight/hotel search.

## Design

### Goals

- Keep each agent's **prompt**, **tools**, and **wiring** easy to find and
  change independently.
- Share setup (API keys, the LLM, the web search tool) in one place instead
  of repeating it per agent.
- Make adding a new agent or tool a copy-paste-and-edit operation, not a
  refactor.

### Components

- **`config.py`** — loads `.env`, exposes API keys, and builds the two
  objects every agent shares: the `llm` (GPT-4o) and the `internet_search`
  tool (Tavily).
- **`tools/`** — one file per external API integration. Currently
  `flights.py` and `hotels.py`, both backed by SerpAPI (Google
  Flights/Hotels). `tools/__init__.py` re-exports them so agents just do
  `from tools import search_flights, search_hotels`.
- **`prompts/`** — one file per agent holding just its system prompt, named
  to match the agent file that uses it (`prompts/travel_scout.py` ↔
  `agents/travel_scout.py`). Keeps long prompt text out of the wiring code.
- **`agents/`** — one file per agent. Each file imports its prompt from
  `prompts/`, imports the tools it needs, and calls `create_agent` /
  `create_deep_agent` to build the agent object. No prompt text and no tool
  implementations live here — just assembly.
- **`app.py`** — entry point. Imports the top-level agent
  (`travel_scout`) and runs one example query.

### Agents

| Agent | File | Role | Tools |
|---|---|---|---|
| **Travel Scout** | `agents/travel_scout.py` | Front door. Answers general travel questions (weather, visas, packing, high-level comparisons). Delegates day-by-day planning to the Itinerary Agent. | `internet_search`, `itinerary_research_agent` (as a tool) |
| **Itinerary Agent** | `agents/itinerary_agent.py` | Deep research + day-by-day itinerary construction. | `internet_search` |
| **Search Agent** | `agents/search_agent.py` | Flight and hotel search with structured inputs. | `search_flights`, `search_hotels` |

The Search Agent is currently invoked directly (not yet wired as a tool
under Travel Scout) — see "Possible extensions" below.

### Request flow

```
                              ┌───────────────────────┐
                    user ───▶ │      Travel Scout       │
                              │ (agents/travel_scout.py)│
                              └───────────┬────────────┘
                                          │
                     general question?   │   needs a day-by-day plan?
                      ┌───────────────────┴───────────────────┐
                      ▼                                        ▼
            ┌───────────────────┐                  ┌─────────────────────────┐
            │  internet_search   │                  │   itinerary_research_    │
            │  (Tavily, shared)  │                  │   agent  (as a tool)     │
            └───────────────────┘                  └────────────┬────────────┘
                                                                  │
                                                                  ▼
                                                      ┌───────────────────────┐
                                                      │    Itinerary Agent      │
                                                      │(agents/itinerary_agent) │
                                                      │  uses internet_search   │
                                                      └───────────────────────┘

            ┌───────────────────────┐
            │     Search Agent        │  ◀── invoked directly today
            │ (agents/search_agent.py)│      (not yet a Travel Scout tool)
            └───────────┬────────────┘
                         │
             ┌───────────┴────────────┐
             ▼                        ▼
     ┌───────────────┐       ┌────────────────┐
     │ search_flights  │       │ search_hotels    │
     │ (tools/flights) │       │ (tools/hotels)   │
     └───────┬────────┘       └────────┬────────┘
             │                          │
             ▼                          ▼
        SerpAPI: Google           SerpAPI: Google
          Flights                   Hotels
```

### File layout

```
travel_agent/
├── app.py                      # entry point: builds a query, prints the answer
├── config.py                   # env vars, shared llm, shared internet_search tool
├── requirements.txt
├── .env                        # OPENAI_API_KEY, TAVILY_API_KEY, SERP_API_KEY (gitignored)
│
├── prompts/                    # system prompts, one file per agent
│   ├── itinerary_agent.py      #   research_instructions
│   ├── search_agent.py         #   flightHotelSearch_instructions
│   └── travel_scout.py         #   travel_scout_instructions
│
├── agents/                     # agent wiring: prompt + tools + model
│   ├── itinerary_agent.py      #   itinerary_research_agent
│   ├── search_agent.py         #   search_agent
│   └── travel_scout.py         #   travel_scout (wraps itinerary agent as a tool)
│
└── tools/                      # external API integrations
    ├── flights.py              #   search_flights (SerpAPI / Google Flights)
    └── hotels.py                #   search_hotels (SerpAPI / Google Hotels)
```

### Conventions for extending this

- **New tool** → add a file to `tools/`, re-export it from
  `tools/__init__.py`.
- **New agent** → add a prompt file to `prompts/`, add an agent file to
  `agents/` that imports the prompt + the tools it needs, and calls
  `create_agent` (or `create_deep_agent` for research-heavy agents).
- **Shared setup** (new API key, new shared tool/model) → add it to
  `config.py`.

### Possible extensions

- Wire `search_agent` as a tool under `travel_scout` (the same pattern used
  for `itinerary_research_agent`) so one entry point can route to all three
  agents.
- Add a CLI/loop in `app.py` instead of the single hardcoded example query.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file (gitignored) with:

```
OPENAI_API_KEY=...
TAVILY_API_KEY=...
SERP_API_KEY=...
```

## Run

```bash
python app.py
```
