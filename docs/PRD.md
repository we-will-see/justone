# PRD — justone

> Status: **draft v3**. Adds a centralised evolving memory layer alongside the modular tool fleet. Sections marked *(extrapolated)* are my reads — push back where they don't match.

## Vision

A modular fleet of mini-agents that mimic your problem-solving patterns at scale. Each agent targets a specific recurring problem distilled from your conversation history across Claude, ChatGPT, and Gemini. Together they act as a personal research analyst — doing what you already do, but in parallel and on demand.

Your chat history is dual-purpose:
1. **Reasoning fingerprint** — how you think, decide, structure tradeoffs. Becomes the style prompt.
2. **Problem catalog** — what you keep working on. Becomes the tool roadmap.

The first informs *how* every tool reasons. The second informs *which tools to build*.

A third substrate accumulates *after* the system goes live:

3. **Evolving memory** — facts, decisions, project context, corrections, and outcomes from every task you run through the fleet. Becomes the runtime context that every tool reads from and the orchestrator writes to.

Together: chat history defines who you are at startup; memory tracks who you become as the system runs.

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
│  All read from memory; all surface findings worth keeping.  │
└─────────────────────────────────────────────────────────────┘
                       ↑↓ read / write
┌─────────────────────────────────────────────────────────────┐
│  EVOLVING MEMORY (centralised, persistent)                  │
│  Facts · decisions · project context · entity registry ·    │
│  past task outcomes · corrections from your feedback        │
│  Read by every tool · written by orchestrator after each    │
│  interaction · curated (what stays, what decays)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (later)                                       │
│  Routes requests · composes tools · updates memory after    │
│  every run                                                  │
└─────────────────────────────────────────────────────────────┘
```

## Goals

1. **Style fidelity** — every tool reasons in your voice, not a generic assistant's.
2. **Modularity** — tools are independent, composable, and addable without rewriting the system.
3. **Multi-source ingestion** — works across Claude, ChatGPT, and Gemini chat exports via a single normalized schema.
4. **Problem-driven tooling** — tools exist because they solve a problem you've actually been solving repeatedly, not because they're cool.
5. **Living memory** — a centralised store that accumulates context from every interaction; tools and orchestrator both consume and contribute to it.
6. **Reproducible & cheap** — runs on free or near-free infra (Kaggle for v1), uses open models (Kimi K2.6 via Together AI), no vendor lock-in.

## Non-goals

- Multi-user product. Single-tenant, self-hosted, personal.
- Hosted SaaS or web UI in v1–v3. Notebook + CLI is fine.
- Fine-tuning. Style and behavior come from prompts, not weight updates.
- General-purpose chatbot replacement. Each tool is narrow on purpose.
- Tool ecosystems beyond `web_search` for the v1 tool.
- Auto-learning that updates memory without your visibility — every memory write should be inspectable and reversible.

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

### Phase D — Centralised evolving memory
- D.1 Decide storage (filesystem JSON · SQLite · DuckDB · vector store)
- D.2 Define memory schema — what kinds of entries exist (facts, decisions, entities, task outcomes, corrections), each with provenance + timestamp
- D.3 Memory API — `read(query, scope)`, `write(entry, source)`, `forget(id)`, `list_recent(n)`
- D.4 Curation policy — what gets written automatically vs. requires explicit `remember(...)` from you, what decays, how conflicts resolve
- D.5 Inspection — every memory entry is auditable; you can see why it was written and what wrote it
- D.6 Wire into existing v1 tool so memory accumulates from real use before tools #2/#3 are built

### Phase E — Build tool #2 and #3 (memory-aware)
- E.1 Pick top two categories from Phase C
- E.2 Spec each tool — inputs, outputs, search/tooling needs, memory read/write patterns
- E.3 Implement: shared style prompt, memory access from day one, evaluate

### Phase F — Orchestrator
- F.1 Define routing — incoming request → which tool(s); memory informs routing decisions
- F.2 Composition — tools that chain (e.g., research → summary → action)
- F.3 Single entry point that dispatches across the fleet and writes session outcomes back to memory

### Phase G — Beyond Kaggle (if needed)
- G.1 Decide whether to keep notebook-based or move to a small Python package + CLI
- G.2 Persistence at scale (memory store outgrows JSON?)
- G.3 Lightweight scheduler for unattended runs

## High-level requirements

| Area | Requirement | Phase |
|---|---|---|
| Style prompt | Extracted from unified conversation set; injected on every tool call. | A → B |
| Conversation schema | Single normalized JSON shape covering Claude, ChatGPT, Gemini exports. | B |
| Tool interface | Each tool: input spec, output spec, optional search/tools, shared style prompt, memory access. | A → E |
| Search | Tavily structured JSON, retry, cache, date filter. | A |
| Model | Kimi K2.6 via Together AI; raw HTTP; tenacity retries. | A |
| Mining | Clustering or LLM-driven categorization over normalized conversations. | C |
| Memory | Centralised, persistent, evolving store with read/write API and curation policy. | D |
| Orchestrator | Request → tool router; tool composition; writes outcomes to memory. | F |
| Secrets | Kaggle secrets (or `.env` if it leaves Kaggle); never hardcoded. | all |

## Open questions

- **Style scope** — one global style prompt, or per-tool style prompts (e.g., the way you write *research* questions vs. *debugging* questions might differ)?
- **Problem mining method** — LLM-driven categorization (cheap, fuzzy) vs. embedding clustering (rigorous, more setup)? Hybrid?
- **Source weighting** — should ChatGPT chats count equally to Claude chats when extracting style, or weight by recency / domain relevance?
- **Tool spec format** — YAML, Python class, JSON schema? This becomes the "API" of the fleet.
- **Memory storage** — JSON file (simple, inspectable) → SQLite (queryable, ACID) → SQLite + embeddings (semantic retrieval). Where to start, when to upgrade?
- **Memory granularity** — atomic facts ("user prefers TypeScript over JS") vs. richer episodes ("on 2026-04-15, user asked about X, we found Y, user pushed back on Z")? Probably both, with cross-references.
- **Memory write authority** — automatic write after every interaction (rich, noisy) vs. explicit `remember(...)` calls only (clean, easily missed) vs. orchestrator decides per-event (judgment call, possibly inconsistent)?
- **Memory decay** — never (everything kept), time-based (drop entries older than X), salience-based (LLM compresses old entries periodically)?
- **Memory conflicts** — when new memory contradicts old: keep both with timestamps and let the reader judge, or actively resolve and supersede?
- **Memory ↔ chat history boundary** — at what point does the original chat history become "just old memory"? Or do they stay separate substrates forever?
- **Composition** — can tools call each other directly, or always through the orchestrator? Affects how independent each tool can be.
- **Long-term runtime** — Kaggle is great for v1 but breaks down past Phase D (persistent memory needs persistent storage). Local + cron? A small server? Defer until forced.
- **Which problems first** — until Phase C runs, the second and third tools are placeholders. Worth a quick manual pass over your recent chats to seed candidate categories before formal mining.

## Glossary

- **Tool / mini-agent** — a narrow agent built around one recurring problem pattern (e.g., research analyst, debugging companion, market scanner). Shares the style prompt, has its own task spec.
- **Style prompt** — system message built from your conversation history. Defines reasoning voice across all tools.
- **Problem catalog** — the set of recurring task categories surfaced from your chats, each a candidate for a dedicated tool.
- **Memory** — centralised, persistent, evolving store of facts, decisions, entities, task outcomes, and corrections accumulated through use. Read by every tool, written by the orchestrator.
- **Curation policy** — the rules deciding what gets written to memory, what stays, what decays, how conflicts resolve.
- **ReAct** — Reason + Act loop. Model alternates between thinking and tool use until it answers.
- **Grounding check** — post-answer pass where the model cites which search result supports each claim.
- **Unified conversation schema** — single normalized JSON shape that ingestion adapters output, regardless of source platform.
