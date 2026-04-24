# Local AI Agent

A locally-hosted AI agent built in Python that routes natural language queries
to tool-specific handlers using a prompt-based function calling architecture.
Runs entirely on-device via LM Studio — no cloud dependencies, no API costs,
no data leaving your machine.

## Architecture
The agent uses a structured prompt to instruct the model to output a JSON
tool call when external data is needed. The Python runtime intercepts that
response, executes the appropriate tool, and feeds the result back to the
model to generate a natural language answer.

## Tools

| Tool | Description |
|---|---|
| `get_current_time` | Returns current date and time |
| `calculate` | Evaluates mathematical expressions safely |
| `search_wikipedia` | Retrieves Wikipedia summaries via REST API |

## Tech Stack

- **Runtime:** Python 3.11
- **LLM Backend:** LM Studio (OpenAI-compatible local API)
- **Model Used:** Mistral 7B Instruct v0.3
- **Libraries:** `openai` `rich` `requests`
- **OS:** Ubuntu (WSL2)

## Why Local?

Running inference locally means full control over the model, zero latency
from network calls, no usage costs, and complete data privacy. This project
demonstrates that production-style agentic pipelines don't require cloud
infrastructure.

## Setup

1. Download and install [LM Studio](https://lmstudio.ai)
2. Load any instruction-tuned model and start the local server on port 1234
3. Clone this repo and install dependencies:

```bash
pip install openai rich requests
python agent.py
```

## Example
 Ask me anything: what is 1337 * 42 + 100?
⚙ Using tool: calculate
✓ Tool result: 56254
Agent: 1337 multiplied by 42 plus 100 equals 56,254.
## About

Built by a self-taught AI developer focused on local LLM deployment,
agentic systems, and fine-tuning. Learning and building in public.

GitHub: [lmcreationsualberta-cloud](https://github.com/lmcreationsualberta-cloud)
