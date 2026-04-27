# Project Tracker

Progress tracker for building the Kimi K2.6 pharma-research agentic workflow.

---

## Phase 1 — Environment Setup

- [ ] Choose notebook platform (Google Colab / Kaggle / Replit)
- [ ] Choose API provider (Together AI or Moonshot's own API)
- [ ] Obtain Kimi K2.6 API key and note the base URL
- [ ] Obtain Tavily or SerpAPI key for web search
- [ ] Confirm Python 3.9+ is available in the notebook
- [ ] Install dependencies: `openai`, `requests`, `beautifulsoup4`

---

## Phase 2 — Basic Kimi K2.6 API Call

- [ ] Add `KIMI_API_KEY` and `KIMI_BASE_URL` as environment variables / notebook secrets
- [ ] Implement the raw HTTP call to `moonshotai/Kimi-K2.6` (`temperature=0.3`, `max_tokens=1024`)
- [ ] Verify a test question returns a valid response
- [ ] Wrap the call into a reusable `kimi_call(messages)` function

---

## Phase 3 — Web Search Tool

- [ ] Add `TAVILY_API_KEY` (or SerpAPI key) as environment variable / notebook secret
- [ ] Implement `web_search(query, max_results=3)` function
- [ ] Test that a sample query returns structured results
- [ ] Handle HTTP errors and empty result sets gracefully

---

## Phase 4 — Agentic Loop

- [ ] Build the 3-step reasoning loop:
  - [ ] Step 1 — Initial Kimi reasoning pass
  - [ ] Step 2 — Trigger `web_search` based on reasoning output
  - [ ] Step 3 — Append search results to message thread and get final answer
- [ ] Verify the full loop runs end-to-end on a sample pharma question
- [ ] Tune `max_tokens` (target: 2048 for final answer step)

---

## Phase 5 — Style Injection from Chat History

- [ ] Prepare / export your past chat history as `your_chats.json`
- [ ] Write the style-extraction snippet to pull your best replies
- [ ] Build `YOUR_STYLE_PROMPT` from those replies
- [ ] Inject `YOUR_STYLE_PROMPT` as the system message in all `kimi_call` invocations
- [ ] Validate that responses reflect your pharma-research reasoning style (molecule → trial status → risk/benefit)

---

## Phase 6 — Final Notebook Polish

- [ ] Organize all cells in logical order (install → secrets → functions → agent loop)
- [ ] Remove any hardcoded credentials
- [ ] Add a top-level cell that explains how to run the notebook
- [ ] Share / save the final notebook to the chosen platform
