# Problem Catalog — automation candidates from chat history

> First-pass categorization of 238 conversations from the Claude export (Jan 2026 → Apr 2026). Method: title-only triage on the 176 substantive conversations (≥4 messages). Confident enough to act on; not yet validated by reading conversation contents. See "Open questions" for what would tighten this.

## TL;DR

You're a **sell-side equity research analyst covering Indian pharma & healthcare**, with the bulk of your Claude usage going into structured, repetitive research workflows. Roughly half your substantive conversations are research-task variants of the same handful of templates. Plus smaller clusters: personal/dating, health/meds, life optimization, and tooling experiments.

The five highest-leverage tools to build, in order:

1. **Earnings update generator** (quarterly, ~20+ names)
2. **Investment note / one-pager builder** (per new coverage)
3. **Financial metric extractor** (every transcript / filing)
4. **Transcript Q&A digest** (every earnings call)
5. **Sector deep-dive scaffolder** (per sub-sector)

These five capture an estimated 60–70% of your work-related Claude volume and are all structurally similar enough to share infrastructure.

## Domain breakdown (rough volume)

| Domain | Approx. conversations | Notes |
|---|---|---|
| Equity research — Indian pharma/healthcare | ~85 | Earnings, valuations, transcripts, sector analysis |
| Dating / Hinge / relationships | ~12 | Mostly Hinge prompt drafting + situation analysis |
| Tooling / automation experiments | ~12 | MCPs, custom skills, scripts, news translation |
| Personal admin / misc Q&A | ~12 | Restaurant menus, hardware buying, app issues |
| Health / meds / biohacking | ~6 | Bupropion, escitalopram, melatonin, peptides |
| Career navigation | ~6 | Resume, appraisals, role transitions |
| Life optimization / introspection | ~5 | Long deep-dive conversations |
| Memory / meta-tooling | ~6 | Personal profile creation, memory exports |
| Speculative / creative writing | ~3 | One-off |

The rest are short / fragmented.

## Tier 1 — high-volume, structured, automatable now

### 1. Earnings Update Generator
**Trigger:** quarterly results drop for a covered name.
**Recurrence in history:** ~25+ conversations. Examples: KIMS 3QFY26, Sun Pharma 3QFY26, Cohance 3QFY26, Mankind 3QFY26, Cipla 3QFY26, Granules 3QFY26, Metropolis Health 3QFY26, Lupin 3QFY26, Aurobindo, Divis, Alkem, Biocon, Torrent, AsterDM, Max Healthcare, Medplus, Eris.
**Inputs:** company name, quarter, links to results PDF + transcript (or attachments).
**Outputs:** structured note covering revenue, margin, segment breakdown, management commentary highlights, variance vs. consensus/estimate, key takeaways, recommendation update.
**Tool sketch:** ingest PDF/transcript → extract financials into a table → run management commentary through transcript-Q&A pattern → emit note in your usual format.
**Memory needs:** prior quarter's note for variance analysis, your model assumptions, your standard note structure.

### 2. Investment Note / One-Pager Builder
**Trigger:** new name being added to coverage, or major thesis update.
**Recurrence:** ~15+ conversations. Examples: Zydus Life investment note structure, Sun Pharma update, Mankind one-pager, Lupin thesis, Sai Life Sciences pitch, Cohance buy case, JB Chemicals thesis, Alembic writeup, GSK domestic, Ajanta framework, Emcure framework.
**Inputs:** company name, target price (optional), thesis angle.
**Outputs:** business overview, key drivers, valuation framework, catalysts, risks, recommendation.
**Tool sketch:** template-driven; pulls metrics from filings, peers from your existing coverage list, valuation from a standard multiple framework.
**Memory needs:** your standard note template, your covered universe and their multiples, sector benchmarks.

### 3. Financial Metric Extractor
**Trigger:** any time a filing/transcript hits and you need numbers in a table.
**Recurrence:** ~15+ conversations. Examples: Aier Eye Hospitals financial metrics extraction, Q4 2025 adjustments extraction, Manipal consolidated revenue reconciliation, key financial metrics from annual reports, Dr Agarwal facility unit economics, ARPOB derivation, Eris Lifesciences Q3FY26 results.
**Inputs:** PDF/URL + which metrics to extract.
**Outputs:** structured table (CSV or markdown), with source page references.
**Tool sketch:** PDF parsing + LLM extraction with strict schema, validation against totals.
**Memory needs:** which metrics matter for which sub-sectors (hospitals vs. pharma vs. CDMO have different KPIs).

### 4. Transcript Q&A Digest
**Trigger:** any earnings call transcript.
**Recurrence:** ~10+ conversations. Examples: Cohance 3QFY26 earnings call analysis, Management questions from recent calls, Extracting key takeaways from transcripts for modeling, Transcript notes categorization by product type, Lupin notes verification.
**Inputs:** transcript URL/text + the themes you care about for that name.
**Outputs:** structured Q&A digest grouped by theme (capacity, pricing, margins, regulatory, etc).
**Tool sketch:** segment transcript by speaker → classify segments by theme → extract management responses on each theme → flag deflections and notable language.
**Memory needs:** your theme taxonomy per company, prior quarters' commentary for change-detection.

### 5. Sector Deep-Dive Scaffolder
**Trigger:** new sub-sector coverage initiation, or quarterly sector recap.
**Recurrence:** ~10+ conversations. Examples: CDMO peer comparison framework, Eye care company acquisitions and investments, Indian sulphur producers, Pharma CDMO capacity and stocking, India business drivers, Private hospital sector investment landscape, In-licensing deals, Peptide biohacking trends, Healthcare expectations.
**Inputs:** sub-sector name (CDMO / eye care / hospitals / peptides / API / etc).
**Outputs:** top players, market structure, key drivers, regulatory backdrop, recent M&A, investment landscape.
**Tool sketch:** sector-specific template + Tavily for current data + your covered names for relevance weighting.
**Memory needs:** your covered universe, prior sector deep-dives for continuity.

## Tier 2 — recurring but lower volume / more contextual

### 6. Hinge Prompt Generator
**Trigger:** profile refresh.
**Recurrence:** ~6 conversations. Examples: Unhinged Hinge one-liners, Improving Hinge dating prompts, Crafting a Witty Hinge Prompt, Attention-Grabbing Hinge Openers, Captivating Hinge Openers, Creative Dating Profile Prompt Ideas.
**Inputs:** your interests, what's worked before, what hasn't.
**Outputs:** 5–10 prompt drafts with rationale.
**Memory needs:** prior prompts that performed, your style, what you don't want to come across as.

### 7. Resume / Appraisal Builder
**Trigger:** annual or role-change events.
**Recurrence:** ~5 conversations. Examples: Year end self appraisal preparation, Refining a generic resume for analyst roles, Equity Research Resume Review, Motivation for RBC job application, Transitioning to Lead Analyst Role.
**Inputs:** prior version + new role spec/year.
**Outputs:** updated version aligned to the role/spec.
**Memory needs:** your work history, achievements log (could itself be a memory category that accrues over time).

### 8. Substack / Newsletter Alpha Tracker
**Trigger:** weekly/monthly cadence.
**Recurrence:** mentioned directly in conversations: "Tracking Substack newsletter stock picks for alpha", "Building a personal insider prediction tracker".
**Inputs:** newsletter list + tracking horizon.
**Outputs:** consolidated picks, performance vs. benchmark, signal strength scoring.
**Memory needs:** picks already tracked, their performance, source reliability over time.

## Tier 3 — interesting but probably one-off, not tools

- Specific company drilldowns that aren't in your repeat coverage
- Calculation verification / spreadsheet checks (helpful but ad hoc)
- Health / meds / biohacking — these need human judgment + doctor, not automation
- Relationship-specific advice — too contextual, low recurrence per situation
- Personal admin (restaurant menus, time-off messages, hardware buying) — each is unique
- Speculative / creative writing — by nature one-off

## Patterns worth surfacing

A few cross-cutting observations from the title scan:

- **You already have automation instincts.** Conversations like "Automating company export tracking", "Chemical name standardization script", "Building an MCP for Indian markets", "Building a personal insider prediction tracker", "Automated news translation to Indian languages", "Comprehensive investment research notebook framework" suggest you've been *trying* to build versions of this fleet manually. The justone fleet is the consolidation of those.
- **Basic Memory is already in your stack.** "Hosting Basic Memory on a VPS" + "💬"-prefixed memory-note titles suggest you're already running an external memory tool. The justone memory layer should probably interoperate with or absorb that, not compete.
- **Quarterly cadence is the strongest signal.** ~25 conversations within ~2 months are quarterly earnings updates. Build this tool first and you immediately compress 25+ tasks/quarter into structured runs.

## Open questions for you to validate

1. **Does the equity-research framing match how you'd describe your day job?** Or is "sell-side analyst" a specific subset of broader work?
2. **Among Tier 1, which would save you the most time *today*?** My ranking above is by volume; yours might be by pain.
3. **Is there a recurring pattern I missed?** Title-only triage will miss anything where the pattern is in the conversation flow but not the title.
4. **Should we deepen this catalog now (read sample conversations from each cluster, refine tool specs) or pick #1 and build it as Tool #2?**
5. **Basic Memory integration** — how do you want the justone memory layer to relate to it? Replace, wrap, or sync?

## Methodology notes

- Source: `data/processed/conversations/index.json` (titles + message counts).
- Filter: ≥4 messages to remove aborted starts. 176 of 238 conversations passed.
- Categorization: manual title scan, single pass.
- Confidence: high on the dominant clusters (volume makes them obvious), lower on the long tail.
- What would tighten this: LLM pass over the first user message of each conversation (extracts the actual ask, not just the auto-generated title) and embedding-based clustering (catches semantic siblings across category boundaries).
