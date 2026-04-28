# justone

A lightweight Kaggle-first repository for building and iterating on a Kimi K2.6 + Tavily agent workflow.

## Quick start

1. Open `notebooks/agent.ipynb` in Kaggle.
2. Add Kaggle secrets:
   - `TOGETHER_API_KEY`
   - `TAVILY_API_KEY`
3. Upload your chat export zip to `data/raw/` (or as a Kaggle dataset input).
4. Run notebook cells top-to-bottom.

## Repository layout

- `notebooks/agent.ipynb` — main workflow notebook.
- `docs/TRACKER.md` — implementation progress checklist.
- `docs/CLAUDE.md` — architecture and implementation notes.
- `docs/README.md` — documentation index and conventions.
- `scripts/repo_health.py` — local status script for quick project visibility.
- `data/raw/` — source JSON + export archives.
- `data/processed/` — generated artifacts.

## Daily maintenance commands

Run these from the repo root:

```bash
make health
make tracker-open
make notebook-open
```

What they do:

- `make health`: prints a quick summary of tracker completion, notebook cell counts, and raw-data files.
- `make tracker-open`: prints tracker content for fast review.
- `make notebook-open`: prints minimal notebook metadata.

## Future cleanup checklist

- Keep all architecture decisions in `docs/` (not notebook comments).
- Keep one source-of-truth checklist in `docs/TRACKER.md`.
- Keep helper automation in `scripts/`.
- Avoid committing generated outputs unless intentionally versioned.
