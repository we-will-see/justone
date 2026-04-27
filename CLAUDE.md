# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**justone** is a tutorial/guide project for building a Kimi K2.6-based agentic workflow targeting pharmaceutical research use cases. The repository currently contains a single `README.md` — there is no runnable source code, build system, or tests yet.

The README describes how to set up and run a minimal agentic loop in a web-based notebook (Google Colab, Kaggle, or Replit) using Kimi K2.6 as the reasoning engine.

## Intended Architecture

The README outlines a Python notebook-based architecture with these components:

1. **LLM client (`kimi_call`)** — Calls the Kimi K2.6 API via an OpenAI-compatible HTTP endpoint (Together AI or Moonshot). Uses `moonshotai/Kimi-K2.6` as the model ID.
2. **Web search tool (`web_search`)** — Queries Tavily or SerpAPI to retrieve current information; results are injected back into the conversation.
3. **Agent loop** — A reasoning → tool-call → reasoning pattern: Kimi reasons first, a search is triggered, results are appended to the message thread, and Kimi produces a final answer.
4. **Style injection** — A system prompt is built from a user's own past chat history to mimic their pharma-research reasoning style.

### API Configuration

| Variable | Purpose |
|---|---|
| `KIMI_API_KEY` | API key from Kimi / Together AI |
| `KIMI_BASE_URL` | Endpoint, e.g. `https://api.together.ai/v1/chat/completions` |
| `TAVILY_API_KEY` | Search API key |

Model call parameters: `temperature: 0.3`, `max_tokens: 1024–2048`.

### Message Format

Standard OpenAI-compatible chat format:
```python
messages = [
    {"role": "system", "content": YOUR_STYLE_PROMPT},
    {"role": "user",   "content": USER_QUESTION},
    # assistant turns and search-result injections appended dynamically
]
```

## Development Notes

- If notebook cells are converted to `.py` files, keep `web_search` and `kimi_call` as separate functions — the README establishes this separation of concerns.
- Credentials must come from environment variables or Colab secrets, never hardcoded.
- The style-extraction step (loading `your_chats.json`) is designed to run once at setup; the extracted `YOUR_STYLE_PROMPT` is then reused across all agent calls.
