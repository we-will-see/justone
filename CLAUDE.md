# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**justone** is a general-purpose agentic workflow built on Kimi K2.6. The agent's reasoning style and behavior are defined entirely by the user's own chat history (`your_chats.json`) — there is no hardcoded domain logic. The target runtime is a **Kaggle notebook**.

The final deliverable is `agent.ipynb` — a self-contained notebook that extracts a style prompt from chat history, then runs a ReAct-style search-augmented loop using Kimi K2.6 and Tavily.

## Architecture

### Components

1. **`kimi_call(messages, max_tokens)`** — Raw HTTP POST to Together AI's OpenAI-compatible endpoint. Model: `moonshotai/Kimi-K2.6`. Wrapped with `@tenacity.retry` (3 attempts, exponential backoff) and a 30s timeout.

2. **`web_search(query, max_results)`** — Tavily search returning structured JSON. Wrapped with the same retry policy, 10s timeout, and an in-memory dict cache keyed by query string.

3. **`count_tokens(text)`** — Lightweight helper (`word_count × 1.3`) used to trim search results before appending to the message thread to avoid context overflow.

4. **`parse_action(text)`** — Extracts `action` and `action_input` from the model's structured output format (pydantic or regex).

5. **ReAct loop** — Max 3 iterations. Each turn the model outputs:
   ```
   Thought: <reasoning>
   Action: web_search | final_answer
   Action Input: <query or answer>
   ```
   On `web_search`: results are trimmed and appended; loop continues. On `final_answer`: a final `kimi_call` with `max_tokens=2048` is made and the loop exits. If max iterations are reached, a forced synthesis call is made.

6. **Style prompt** — Extracted once from `your_chats.json` at notebook startup. Injected as the `system` message on every `kimi_call`. This is what defines the agent's behavior — do not replace it with hardcoded domain prompts.

### API Configuration

| Variable | Value |
|---|---|
| `KIMI_API_KEY` | Together AI key — store as Kaggle secret |
| `KIMI_BASE_URL` | `https://api.together.ai/v1/chat/completions` |
| `TAVILY_API_KEY` | Tavily key — store as Kaggle secret |

Model call parameters: `temperature: 0.3`, `max_tokens: 512` (reasoning steps) / `2048` (final answer).

### Message Format

```python
messages = [
    {"role": "system", "content": YOUR_STYLE_PROMPT},  # extracted from your_chats.json
    {"role": "user",   "content": USER_QUESTION},
    # assistant reasoning turns and search results appended dynamically
]
```

## Development Notes

- Credentials must come from Kaggle secrets, never hardcoded — set this up before writing any code.
- `beautifulsoup4` is not needed; Tavily returns structured JSON.
- The style-extraction cell runs once at startup; `YOUR_STYLE_PROMPT` is reused for the full session.
- Keep `kimi_call`, `web_search`, `count_tokens`, and `parse_action` as separate functions even if the notebook is later split into `.py` files.
- Tavily queries should include a date filter (after 2022) and the grounding check (model cites sources) should run after every final answer.
