#  Local AI Agent

A Python AI agent that runs 100% locally using LM Studio — no cloud, no API costs.

## What It Does
Ask it anything and it decides which tool to use on its own:
- **Time** — tells you the current date and time
-  **Calculator** — solves math expressions
- **Wikipedia** — searches and summarizes any topic

## How It Works
1. You ask a question
2. The agent reads it and decides if it needs a tool
3. It runs the tool and uses the result to form a final answer

## Requirements
- [LM Studio](https://lmstudio.ai) running locally with any model loaded
- Python 3.11+

## Setup
```bash
pip install openai rich requests
python agent.py
```

## Built By
Self-taught AI developer — learning in public.
