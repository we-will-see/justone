# Project Tracker

Progress tracker for building the Kimi K2.6 general-purpose agentic workflow.

---

## Phase 1 — Environment Setup

- [x] Platform: Kaggle
- [x] API provider: Together AI (`https://api.together.ai/v1/chat/completions`, model `moonshotai/Kimi-K2.6`)
- [x] Search API: Tavily
- [ ] Obtain Together AI API key; confirm `moonshotai/Kimi-K2.6` is listed in their model catalog
- [ ] Obtain Tavily API key
- [ ] Add both keys as **Kaggle secrets** (before writing any code — never hardcode)
- [x] Install dependencies: `requests`, `tenacity`, `pydantic` (drop `beautifulsoup4` — Tavily returns structured JSON; `openai` SDK optional since we use raw HTTP)

---

## Phase 2 — Core API Functions with Hardening

- [ ] Implement `kimi_call(messages, max_tokens=512)`:
  - Explicit `timeout=30` on the HTTP call
  - `@tenacity.retry` with exponential backoff (3 attempts, 2→4→8s) on 429/5xx
  - Raises on unexpected response shape
- [ ] Implement `web_search(query, max_results=5)`:
  - Explicit `timeout=10`
  - Same retry policy
  - In-memory cache (dict keyed by query) to avoid re-burning quota while iterating
- [ ] Write `count_tokens(text)` helper (word count × 1.3 heuristic) for trimming search results before appending to context
- [ ] Smoke-test both functions independently

---

## Phase 3 — Style Extraction from Chat History

- [ ] Upload `your_chats.json` to Kaggle dataset or notebook working directory
- [ ] Write extraction snippet to load the file and pull representative responses
- [ ] Build `YOUR_STYLE_PROMPT` from those replies — this becomes the system message that defines ALL agent behavior
- [ ] Validate the prompt produces responses that match your expected reasoning patterns on 2–3 test questions

---

## Phase 4 — ReAct Agentic Loop

- [ ] Define structured turn format the model must output:
  ```
  Thought: <reasoning>
  Action: web_search | final_answer
  Action Input: <query or final text>
  ```
- [ ] Implement `parse_action(text)` (pydantic or regex) to extract `action` and `action_input`
- [ ] Build the loop (max 3 iterations):
  - [ ] Call `kimi_call` with `max_tokens=512` for reasoning steps
  - [ ] If `action == "web_search"`: call `web_search`, trim results to fit token budget, append to messages, loop
  - [ ] If `action == "final_answer"`: call `kimi_call` with `max_tokens=2048`, exit loop
  - [ ] If max iterations hit without `final_answer`: force a final synthesis call
- [ ] Add date filter to Tavily queries (results after 2022) for freshness
- [ ] Grounding check: after final answer, ask model to cite which search result supports each claim

---

## Phase 5 — Benchmark & Evaluate

- [ ] Prepare 5 representative questions in the domain you actually use the agent for
- [ ] Run all 5 through the full loop
- [ ] Score each: does the output match your expected reasoning style? Are citations present?
- [ ] Fix any systematic failures before moving to polish

---

## Phase 6 — Final Notebook Polish

- [ ] Decide output artifact: print to cell output, save to CSV, or both
- [ ] Organize cells: install → secrets → helper functions → style extraction → agent loop → benchmark runner
- [ ] Add a single markdown cell at top explaining how to run
- [ ] Commit final notebook to repo as `agent.ipynb`
