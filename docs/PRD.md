# PRD — justone

> Status: **draft v2**. Vision rewritten after owner clarification: this is a modular tool factory, not a single agent. Sections marked *(extrapolated)* are my reads — push back where they don't match.

## Vision

A modular fleet of mini-agents that mimic your problem-solving patterns at scale. Each agent targets a specific recurring problem distilled from your conversation history across Claude, ChatGPT, and Gemini. Together they act as a personal research analyst — doing what you already do, but in parallel and on demand.

Your chat history is dual-purpose:
1. **Reasoning fingerprint** — how you think, decide, structure tradeoffs. Becomes the style prompt.
2. **Problem catalog** — what you keep working on. Becomes the tool roadmap.

The first informs *how* every tool reasons. The second informs *which tools to build*.

## Target user

One: you. The agent fleet exists to multiply *your* throughput on the recurring research and analysis tasks you already do manually.

## Problem

- Generic LLMs answer one question at a time, in a generic voice, without memory of how you've approached similar problems before.
- Your chat history across Claude, ChatGPT, and Gemini already shows the patterns — what you research, how you decompose problems, what you treat as obvious vs. uncertain — but it's locked inside three different export formats.
- Hand-writing system prompts captures surface tone but not actual problem-solving structure.
- Even with a good single agent, you'd still be running every task one-off. The leverage is in turning the recurring patterns into dedicated tools that run on demand.

## Core architecture *(extrapolated — confirm direction)*

```
┌─────────────────────────────────────────────────────────────┐
│  INGESTION LAYER                                            │
│  Claude export · ChatGPT export · Gemini export             │
│       ↓                                                     │
│  Normalize → unified conversation schema                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  MINING LAYER                                               │
│  - Style extraction → reasoning fingerprint (system prompt) │
│  - Problem clustering → recurring task categories           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  TOOL LAYER (the fleet)                                     │
│  Tool #1: research analyst (ReAct + Tavily)  ← v1, current  │
│  Tool #2: ?                                                 │
│  Tool #3: ?                                                 │
│  ...                                                        │
│  All share the style prompt; each has its own task spec.    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (later)                                       │
│  Route incoming request → right tool · compose if needed    │
└─────────────────────────────────────────────────────────────┘
```

## Goals

1. **Style fidelity** — every tool reasons in your voice, not a generic assistant's.
2. **Modularity** — tools are independent, composable, and addable without rewriting the system.
3. **Multi-source ingestion** — works across Claude, ChatGPT, and Gemini chat exports via a single normalized schema.
4. **Problem-driven tooling** — tools exist because they solve a problem you've actually been solving repeatedly, not because they're cool.
5. **Reproducible & cheap** — runs on free or near-free infra (Kaggle for v1), uses open models (Kimi K2.6 via Together AI), no vendor lock-in.

## Non-goals

- Multi-user product. Single-tenant, self-hosted, personal.
- Hosted SaaS or web UI in v1–v3. Notebook + CLI is fine.
- Fine-tuning. Style and behavior come from prompts, not weight updates.
- General-purpose chatbot replacement. Each tool is narrow on purpose.
- Real-time conversation memory across sessions (until v3+).
- Tool ecosystems beyond `web_search` for the v1 tool.

## Success criteria

### v1 (research analyst notebook — current)
- 5 representative questions through the ReAct loop, each producing (a) style-consistent reasoning, (b) at least one Tavily citation, (c) terminating within iteration cap or forced synthesis.
- Blind read of agent output passes a "could I have written this?" gut check.

### v2+ (fleet)
- Three or more recurring problem categories surfaced from chat mining, each backed by a dedicated tool.
- Adding a new tool requires no changes to ingestion, mining, or style layers — only a new task spec and tool-side prompt.
- Multi-source ingestion produces a unified conversation set that style extraction and mining run against, regardless of which platform a chat came from.

## Phased plan

### Phase A — v1: First tool (in progress)
Build the research-analyst tool as a Kaggle notebook. This is the prototype for what every later tool will look like.

- A.1 Environment + hardened API helpers ✅
- A.2 Style extraction from `your_chats.json` ✅ (validation review pending)
- A.3 ReAct loop with grounding check (next)
- A.4 5-question benchmark
- A.5 Notebook polish

(See `docs/TRACKER.md` for line-item status.)

### Phase B — Multi-source ingestion
- B.1 Define unified conversation schema (one JSON shape regardless of source)
- B.2 Adapter for Claude export (current)
- B.3 Adapter for ChatGPT export
- B.4 Adapter for Gemini export
- B.5 Merge + dedupe across sources

### Phase C — Problem mining
- C.1 Topic/intent clustering across the unified conversation set
- C.2 Surface top N recurring problem categories
- C.3 For each category: example prompts, frequency, and rough tool spec

### Phase D — Build tool #2 and #3
- D.1 Pick top two categories from Phase C
- D.2 Spec each tool (inputs, outputs, search/tooling needs)
- D.3 Implement, share style prompt, evaluate

### Phase E — Orchestrator
- E.1 Define routing — incoming request → which tool(s)
- E.2 Composition — tools that chain (e.g., research → summary → action)
- E.3 Single entry point that dispatches across the fleet

### Phase F — Beyond Kaggle (if needed)
- F.1 Decide whether to keep notebook-based or move to a small Python package + CLI
- F.2 Persistence (where do tool runs and findings live?)
- F.3 Lightweight scheduler for unattended runs

## High-level requirements

| Area | Requirement | Phase |
|---|---|---|
| Style prompt | Extracted from unified conversation set; injected on every tool call. | A → B |
| Conversation schema | Single normalized JSON shape covering Claude, ChatGPT, Gemini exports. | B |
| Tool interface | Each tool: input spec, output spec, optional search/tools, shared style prompt. | A → D |
| Search | Tavily structured JSON, retry, cache, date filter. | A |
| Model | Kimi K2.6 via Together AI; raw HTTP; tenacity retries. | A |
| Mining | Clustering or LLM-driven categorization over normalized conversations. | C |
| Orchestrator | Request → tool router; later, tool composition. | E |
| Secrets | Kaggle secrets (or `.env` if it leaves Kaggle); never hardcoded. | all |

## Open questions

- **Style scope** — one global style prompt, or per-tool style prompts (e.g., the way you write *research* questions vs. *debugging* questions might differ)?
- **Problem mining method** — LLM-driven categorization (cheap, fuzzy) vs. embedding clustering (rigorous, more setup)? Hybrid?
- **Source weighting** — should ChatGPT chats count equally to Claude chats when extracting style, or weight by recency / domain relevance?
- **Tool spec format** — YAML, Python class, JSON schema? This becomes the "API" of the fleet.
- **Storage** — filesystem (current) is fine through Phase C, but Phase D+ likely needs something queryable. SQLite? DuckDB?
- **Composition** — can tools call each other directly, or always through the orchestrator? Affects how independent each tool can be.
- **Long-term runtime** — Kaggle is great for v1 but breaks down past Phase D (multiple tools, possibly background runs). Local + cron? A small server? Defer until forced.
- **Which problems first** — until Phase C runs, the second and third tools are placeholders. Worth a quick manual pass over your recent chats to seed candidate categories before formal mining.

## Glossary

- **Tool / mini-agent** — a narrow agent built around one recurring problem pattern (e.g., research analyst, debugging companion, market scanner). Shares the style prompt, has its own task spec.
- **Style prompt** — system message built from your conversation history. Defines reasoning voice across all tools.
- **Problem catalog** — the set of recurring task categories surfaced from your chats, each a candidate for a dedicated tool.
- **ReAct** — Reason + Act loop. Model alternates between thinking and tool use until it answers.
- **Grounding check** — post-answer pass where the model cites which search result supports each claim.
- **Unified conversation schema** — single normalized JSON shape that ingestion adapters output, regardless of source platform.
