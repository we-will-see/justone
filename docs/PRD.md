# PRD — justone

> Status: **draft**. Vision section is my read of intent based on existing code and docs — challenge anything that doesn't match.

## Vision

A personal, web-grounded reasoning agent that thinks in *your* voice. Style is cloned from your own Claude chat export (`your_chats.json`), not engineered through prompt templates. The whole thing fits in a single Kaggle notebook and runs on free infrastructure — no hosting, no fine-tuning, no vendor lock-in.

The bet: **a small style prompt extracted from real conversation history beats a long, hand-written persona prompt** for producing answers that feel like your own reasoning rather than a generic assistant's.

## Target user

One: you. The repo is reproducible enough that someone else could fork it, drop in their own chat export, and get an agent that reasons like them — but that's a side effect, not the product.

## Problem

Generic LLM assistants reason in a generic voice. Hand-written system prompts ("be concise, be skeptical, prefer bullet points...") capture surface tone but not actual reasoning patterns: how you decide what to look up, what you treat as obvious, what you flag as uncertain, how you structure tradeoffs. Months of your real chats encode all of that implicitly.

## Goals

1. **Style fidelity** — agent answers feel like extensions of your own thinking, not mimicry of a prompt template.
2. **Grounded answers** — every factual claim backed by a Tavily search result, with a post-hoc citation pass.
3. **Single-file deliverable** — `notebooks/agent.ipynb` runs top-to-bottom on Kaggle with two secrets and a chat export. No external services beyond Together AI + Tavily.
4. **Reproducible from scratch** — anyone with the repo, two API keys, and their own chat export can rebuild the agent in under 30 minutes.

## Non-goals

- Fine-tuning or training. Style is prompt-only.
- A web UI, hosted endpoint, or multi-user product.
- Domain-specific logic. The agent is general-purpose; domain emerges from the questions you ask it.
- Long-running memory across sessions. Each notebook run is stateless.
- Tool ecosystems beyond `web_search` + `final_answer` for v1.

## Success criteria

- Run 5 representative questions through the full ReAct loop. For each: (a) reasoning style matches your expectations, (b) at least one Tavily citation supports the final answer, (c) loop terminates within the 3-iteration cap or a forced synthesis.
- A blind test (you reading the agent's output cold) — you'd plausibly mistake it for something you wrote.
- Notebook runs end-to-end on a fresh Kaggle session in under 5 minutes for a single question.

## High-level requirements

| Area | Requirement |
|---|---|
| Model | Kimi K2.6 via Together AI (`moonshotai/Kimi-K2.6`), `temperature=0.6`, raw HTTP. |
| Search | Tavily structured JSON, in-memory cache, 10s timeout, retry on 429/5xx. |
| Style | Extracted once from `your_chats.json` at startup; injected as `system` on every call. |
| Loop | ReAct, max 3 iterations, forced synthesis on overflow. |
| Grounding | Post-answer citation pass — model maps each claim to a search result. |
| Freshness | Tavily date filter (results after 2022). |
| Hardening | Tenacity retries, explicit timeouts, response-shape validation. |
| Secrets | Kaggle secrets only — never hardcoded. |

## Out of scope (for v1)

- Streaming responses
- Multi-turn conversation memory
- Tool calling beyond search (no code execution, no file I/O for the agent itself)
- Evaluation harness beyond the manual 5-question benchmark
- Splitting the notebook into a Python package

## Phased plan (mirrors `docs/TRACKER.md`)

1. **Environment setup** — Kaggle secrets, deps. ✅
2. **Hardened API helpers** — `kimi_call`, `web_search`, `count_tokens`. ✅
3. **Style extraction** — load chat export, build `YOUR_STYLE_PROMPT`, validate. (validation review pending)
4. **ReAct loop** — `parse_action`, 3-iteration loop, grounding check.
5. **Benchmark** — 5 representative questions, score for style + citations.
6. **Polish** — final notebook organized, README updated, output artifact decided.

## Open questions

- **Style extraction strategy** — currently pulls "representative responses" from the chat export. Worth defining what "representative" means: longest? most recent? topically diverse? A reproducible selection rule beats ad-hoc filtering.
- **Output artifact** — print to cell, save to CSV, or both? Decision deferred to Phase 6 but worth pinning before benchmark runs so results are comparable.
- **Eval beyond manual review** — is a 5-question manual benchmark enough, or do we want a small automated harness (style-similarity scoring against held-out chats)?
- **Distribution** — does this stay a personal Kaggle notebook, or eventually become a public template repo with `your_chats.json` as the only swap-in?

## Glossary

- **Style prompt** — the `system` message built from your chat export. Defines all agent behavior.
- **ReAct** — Reason + Act loop. Model alternates between thinking and tool use until it decides to answer.
- **Grounding check** — post-answer pass where the model cites which Tavily result supports each claim.
