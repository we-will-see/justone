# justone

## What this repo is
This repository is a working notebook project for building a **Kimi K2.6-powered agentic workflow** for research-style Q&A.

The main deliverable is a runnable notebook (`agent.ipynb`) that:
- Calls Kimi K2.6 through Together AI.
- Uses Tavily web search as a tool.
- Mimics your response style using exported chat history.
- Iterates toward a grounded final answer.

## Current status
- ✅ **Completed:** Phase 1 (environment setup) and Phase 2 (core API + hardening).
- 🟨 **In progress:** Phase 3 (style extraction) — extraction scaffold is done, style-alignment validation remains.
- ⬜ **Not started / pending:** Phase 4 (ReAct loop), Phase 5 (benchmarking), and Phase 6 (notebook polish).

For the full checklist and roadmap details, see **[`docs/TRACKER.md`](docs/TRACKER.md)**.

## Repo layout
- `README.md` — quick-start overview (this file).
- `docs/TRACKER.md` — detailed phase-by-phase roadmap and checklist.
- `agent.ipynb` — primary notebook implementation.
- `users.json` / `projects.json` — structured data files used by notebook experiments.
- `data-c1ba222c-657a-450d-81f2-39ab5b6e8a30-1777329463-8a99ef2f-batch-0000.zip` — current chat export archive example.

## Prerequisites
- Kaggle notebook environment (recommended per tracker).
- Python 3.9+.
- API keys stored as Kaggle Secrets (do **not** hardcode):
  - `TOGETHER_API_KEY`
  - `TAVILY_API_KEY`
- Python packages used in notebook steps:
  - `requests`
  - `tenacity`
  - `pydantic`

## How to run notebook
1. Open `agent.ipynb` in Kaggle.
2. Add required secrets in Kaggle (Settings → Secrets):
   - `TOGETHER_API_KEY`
   - `TAVILY_API_KEY`
3. Ensure required input files are present in the locations listed below.
4. Run cells in order:
   - dependency/install setup
   - secrets and config
   - API helper functions (`kimi_call`, `web_search`, token trim helper)
   - style extraction from chat export
   - agent loop / evaluation cells

## Input data format
Required and expected input locations in this repo:

1. **Chat export ZIP**
   - Place at repo root:  
     `./data-c1ba222c-657a-450d-81f2-39ab5b6e8a30-1777329463-8a99ef2f-batch-0000.zip`
   - If you use a different file name, update the notebook cell that references the archive path.

2. **Extracted/normalized chat JSON**
   - Place at repo root as:  
     `./your_chats.json`
   - Expected shape: JSON array/object containing prior assistant/user messages that can be sampled to construct `YOUR_STYLE_PROMPT`.

3. **Optional structured context files**
   - `./users.json`
   - `./projects.json`

## Output expectations
When the notebook is functioning end-to-end, expected outputs are:
- A style-conditioned response flow (reasoning behavior aligned to extracted chat style).
- Tool-grounded responses that include evidence from Tavily search results.
- A final concise answer per query; optionally saved/exported in later polish phase.
- Reproducible benchmark runs for a fixed question set (planned in roadmap).

For milestone-specific acceptance criteria, use `docs/TRACKER.md` as the source of truth.
