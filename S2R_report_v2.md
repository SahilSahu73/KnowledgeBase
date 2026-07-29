# S2R — Signal to Response
### Platform Status, Architecture & Business Roadmap Report

**Prepared by:** Sahil Sahu (sahil.sahu@esds.co.in)
**Date:** 2 July 2026
**Built:** solo, end to end — architecture, all 24 services, both UIs, infra/ops
**Phases shipped:** 01–29

---

## 1. Executive Summary

S2R watches the public internet — news, developer chatter, job postings, stock-exchange
filings, government tenders — for signs that an Indian enterprise is under IT pain that
ESDS can solve. It scores buying intent with LLMs, builds a live map of the company and
people behind every signal, and is now drafting the outreach that turns a signal into a
conversation, with a human approving every message before it goes out.

| Metric | Value |
|---|---|
| Signals scored to date | **1,505** |
| Companies tracked | **2,390** |
| Contacts identified | **2,331** |
| Live data sources | **7** (4 added in the last cycle) |
| Outreach campaigns opened | **189** |
| Drafts awaiting human review | **75** |
| Confirmed high-intent signals | **316** (21% of all signals scored) |

Everything described in this report — the pipeline, the scraping engineering needed to
get past exchange/government anti-bot defenses, the LLM-driven research-and-draft agent,
and the customer-facing product shell — was designed and built end to end by one person.

---

## 2. Business Objective

**The problem today:** ESDS's highest-value leads — a company migrating to the cloud,
scaling GPU workloads, recovering from a security incident, or issuing a government IT
tender — are announced publicly, in fragments, across dozens of disconnected sources,
often weeks before an RFP is ever issued. Finding them today means a person manually
scanning news, LinkedIn, and portals, then researching the company and writing outreach
by hand — a process that doesn't scale past a handful of leads a day and, by nature,
reacts *after* a competitor has already made contact.

**What S2R changes:**

1. **Detect earlier.** Catch the buying signal at the moment it becomes public — a hiring
   post for a cloud architect, a capex filing, a live tender — instead of waiting for an
   inbound RFP.
2. **Cover exhaustively.** Read and judge every article, filing, and tender across 7
   sources, continuously, at a scale no manual process can sustain.
3. **Qualify automatically.** Separate genuine buying intent from noise using an LLM
   judgment layer, not a keyword match — so the sales team's time goes to real
   opportunities, not false positives.
4. **Act faster.** Move from "signal detected" to "personalized message drafted and ready
   for approval" without a human having to research the company or write the first draft.
5. **Compound the asset.** Every company and person the pipeline touches is resolved,
   deduplicated, and stored — the platform gets more valuable every day it runs, becoming
   an internal intelligence graph ESDS owns outright.

**Primary objective:** compress the time between *a company signals IT pain publicly* and
*ESDS's first personalized outreach* from weeks to hours — without adding headcount.

**Secondary objectives:** competitor visibility (19 competitors tracked, 295 of their
market events logged), a defensible proprietary lead database, and — once the trending
and social-listening sources ship — market visibility beyond just "who is buying."

---

## 3. What S2R Does, In Plain Terms

Think of S2R as a always-on analyst team that never sleeps: one analyst reads every news
article, another reads Hacker News, another watches job boards, two more watch the stock
exchanges' filings, and one watches every government IT tender as it's posted. Each of
them flags anything that looks like an ESDS opportunity, a second-opinion analyst (the
LLM triage layer) confirms whether it's real, and — for the strongest signals — a research
assistant looks up the company and the right person to talk to, then drafts a first
message. A human salesperson only has to read the draft and click Approve.

---

## 4. System Architecture

The platform is built as an assembly line, not a single script — every stage (fetch,
clean, filter, score, decide, act) is its own independently-deployable service, so a bad
day on one source (a blocked scraper, a bad API response) never stalls the rest of the
pipeline. Below, the architecture is split into four layers so each can be understood — and
diagrammed — on its own.

Each subsection includes a ready-to-use **image-generation prompt**: paste the fenced
block into ChatGPT (or any image model) to get a clean architecture diagram for that layer.

### 4A. Data Ingestion Layer

Seven independent ingestor services, each owning one source end to end: fetch → archive
raw → publish an event. Three of them (NSE, BSE, GeM) have to defeat active anti-bot
protection, so they run through a stealth browser instead of a plain HTTP client.

```
[NewsData.io + 10 RSS feeds] ─┐
[Hacker News API]             ─┤
[Jooble API — job postings]   ─┤
[NSE — stock filings]  ──(Camoufox stealth browser)──┐
[BSE — stock filings]  ──(Camoufox stealth browser)──┼─► [MinIO: raw object archive]
[GeM — govt tenders]   ──(Camoufox stealth browser)──┘         │
[CPPP — govt tenders, planned, not yet live] ─┘                 ▼
                                                    [Redpanda event stream]
                                                     topic: crawl.items.raw
                                                                 │
                                                                 ▼
                                                   (continues to Layer B)
```

**Image-generation prompt — Diagram A:**
```text
Create a clean, professional software-architecture diagram, left-to-right flow,
whitepaper style, light background, sans-serif labels, rounded-rectangle nodes,
thin arrows with small arrowheads. No 3D, no photorealism, generous white space.

Title at top: "S2R — Data Ingestion Layer"

Left column: seven separate rounded-rectangle nodes, stacked vertically, light-blue
fill, navy border, each labeled exactly:
  1. "NewsData.io + 10 RSS Feeds (news)"
  2. "Hacker News API"
  3. "Jooble API (job postings)"
  4. "NSE — Stock Exchange Filings"
  5. "BSE — Stock Exchange Filings"
  6. "GeM — Government Tenders"
  7. "CPPP — Government Tenders" — draw this one with a DASHED border and a small
     label underneath reading "planned, not yet live"

Between nodes 4, 5, and 6 and the next column, draw a small pill-shaped label reading
"Camoufox stealth browser" in amber, indicating those three sources route through a
browser-automation layer to bypass anti-bot protection before reaching the pipeline.

All seven left-column nodes have arrows pointing right into one large node in the
middle column labeled "MinIO — Raw Object Archive" (amber/orange fill), with a small
annotation beneath it: "every raw payload archived first — replayable, nothing lost."

One arrow from the MinIO node points right to a final node labeled "Redpanda Event
Stream (Kafka-compatible)" (purple fill), annotated "topic: crawl.items.raw".

An arrow exits the right edge of the canvas from the Redpanda node, labeled
"continues to Core Processing Pipeline →", pointing off-page.
```

---

### 4B. Core Signal Processing Pipeline

Once an event is published, it moves through crawling, cleaning, and scoring before
landing in the console.

```
[Redpanda: crawl.items.raw]
            │
            ▼
   [Crawler service]
   (fetches full article body;
    falls back to Camoufox stealth
    browser if a site blocks plain HTTP)
            │
            ▼
 [Filter / Dedup service]
   - keyword pre-filter (skipped for
     jobs/tenders/filings — already
     pre-qualified at the source)
   - MinHash fingerprint dedup
   - pgvector semantic near-dup check
            │
            ▼
    [LLM Triage service]
  final_score = clip01(0.30 × deterministic_fit
                      + 0.70 × llm_intent_score)
  confirmed:  confidence="confirmed" AND score ≥ 0.65
  uncertain:  score ≥ 0.35
  discarded:  below 0.35
            │
            ▼
   [Persistence service]
  resolves + dedupes company & person
  entities, writes core.signals_new
            │
            ├──────────────► [Signal Console — human-facing UI]
            │
            ▼ (if confirmed + matches roster)
   (continues to Agentic Outreach Flow — Diagram C)
```

**Image-generation prompt — Diagram B:**
```text
Create a clean, professional software-architecture diagram, top-to-bottom vertical
flow, whitepaper style, light background, sans-serif labels, rounded-rectangle nodes,
thin arrows with small arrowheads. No 3D, no photorealism.

Title at top: "S2R — Core Signal Processing Pipeline"

Draw five stacked rounded-rectangle nodes connected by downward arrows, in this order:

1. "Redpanda: crawl.items.raw" (purple fill) — the entry point.
2. "Crawler Service" (blue fill), with a small side-note bubble attached reading
   "falls back to Camoufox stealth browser if blocked"
3. "Filter / Dedup Service" (blue fill), with three small bullet annotations beside it:
   "keyword pre-filter (skipped for jobs/tenders/filings)", "MinHash fingerprint dedup",
   "pgvector semantic near-duplicate check"
4. "LLM Triage Service" (teal fill, slightly larger box), with a formula written
   inside or directly beneath it in monospace font:
   "final_score = 0.30 × deterministic_fit + 0.70 × llm_intent_score"
   and three small labeled outcome arrows branching from it to three small pill labels:
   "Confirmed (score ≥ 0.65)" in green, "Uncertain (score ≥ 0.35)" in amber,
   "Discarded (below 0.35)" in grey
5. "Persistence Service" (blue fill), annotated "resolves & dedupes company + person
   entities"

From the Persistence node, draw two arrows: one pointing right to a node labeled
"Signal Console (human-facing UI)" (light-grey fill), and one pointing down and
labeled "if confirmed + matches target roster" continuing to a node labeled
"Agentic Outreach Flow →" (green fill) which exits the bottom of the canvas.
```

---

### 4C. Agentic Outreach & Research Flow

This is where a confirmed signal turns into a drafted, personalized message — the
"agentic" part of the platform, detailed further in Section 7.

```
[Confirmed signal, matches target/prospect roster]
            │
            ▼
    [Outreach Gate]
  eligibility check + buying-window timing
  → opens ONE live campaign per company
  (5 signals about the same company fold
   into a single thread, not 5 campaigns)
            │
            ▼
  [Contact Resolution]
  existing contacts → Apollo enrichment
  for missing roles
            │
            ▼
     [Researcher agent]
  builds a dossier: firmographic data +
  company website + LinkedIn/X activity
            │
            ▼
       [Judge agent] ◄───────────────┐
    (LLM decision, 3 possible paths)  │
      │            │            │      │
      ▼            ▼            ▼      │
   "Draft"   "Research more"  "Defer" ─┘
      │            │ (loop back once)   │
      │            ▼                    │
      │      [Judge re-decides]         │
      │                                 ▼
      ▼                        recheck timer,
 [Drafter agent]                up to 4 cycles,
  writes personalized                then expires
  email + LinkedIn
  message per contact
      │
      ▼
[Human Review Queue — Signal Console]
   (nothing sends without approval)
      │
      ▼ approve
 [Sender service — SMTP]
      │
      ▼
 [Send Log — auditable record]
```

**Image-generation prompt — Diagram C:**
```text
Create a clean, professional software-architecture / decision-flow diagram, mostly
top-to-bottom with one branching decision point, whitepaper style, light background,
sans-serif labels, rounded-rectangle nodes for services and diamond shapes for
decision points, thin arrows with small arrowheads and text labels on the branches.

Title at top: "S2R — Agentic Outreach & Research Flow"

Sequence, top to bottom:
1. Start node: "Confirmed Signal (matches target roster)" — green fill, pill-shaped.
2. Down-arrow to "Outreach Gate" (blue box), annotated "one live campaign per company".
3. Down-arrow to "Contact Resolution (Apollo enrichment)" (blue box).
4. Down-arrow to "Researcher Agent" (teal box), annotated "builds dossier: firmographic
   data + company website + LinkedIn/X activity".
5. Down-arrow to a DIAMOND decision node labeled "Judge Agent (LLM decision)".

From the diamond, draw three branching arrows:
  a. Labeled "Draft" (green) → box "Drafter Agent — writes personalized email +
     LinkedIn message" → down-arrow to box "Human Review Queue (Signal Console)"
     → down-arrow labeled "Approve" → box "Sender Service (SMTP)" → down-arrow to
     final box "Send Log (auditable record)".
  b. Labeled "Research More" (amber) → small box "One more targeted research pass"
     → curved arrow looping BACK UP to the "Judge Agent" diamond, labeled
     "re-decide, once".
  c. Labeled "Defer" (grey) → box "Recheck Timer — up to 4 cycles" → curved arrow
     looping back to the "Judge Agent" diamond, labeled "retry on schedule", with a
     second small arrow branching off to a final grey box "Expired" for campaigns
     that exceed 4 cycles.

Use green for the positive/success path, amber for the "needs more info" path, and
grey for the "waiting/expired" path, so the three outcomes are visually distinct.
```

---

### 4D. Infrastructure & Platform Layer

Everything above runs on a fully self-hosted stack — no managed cloud services, full cost
and data control.

```
┌─────────────────────────────────────────────────────────────┐
│                     Platform Infrastructure                  │
│                                                               │
│  [Redpanda]        Kafka-compatible event streaming between   │
│                     every pipeline stage                      │
│                                                               │
│  [ParadeDB]         Postgres 17 + pgvector + pg_search —       │
│                     relational data, embeddings, and full-     │
│                     text search in one database                │
│                                                               │
│  [MinIO]            Object storage — raw archive, 90-day        │
│                     retention, ~34 GB across ~296K objects       │
│                                                               │
│  [Temporal]         Durable cron scheduling + human-in-the-loop │
│                     pause/resume                                │
│                                                               │
│  [LiteLLM]          Self-hosted LLM gateway — OpenAI primary,   │
│                     Groq automatic fallback, full cost control  │
│                                                               │
│  [Langfuse]         LLM call tracing & cost observability        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
        24 containerized services · 28 schema migrations
        18,755 lines of Python · 5,250 lines of TypeScript/React
```

**Image-generation prompt — Diagram D:**
```text
Create a clean, professional infrastructure diagram, whitepaper style, light
background, sans-serif labels. Draw one large outer rounded rectangle labeled
"Platform Infrastructure — fully self-hosted" as a container/frame.

Inside it, arrange six smaller rounded-rectangle nodes in a 2-column, 3-row grid,
each with a bold title and a one-line description beneath in smaller grey text:

  Row 1, left: "Redpanda" — "Kafka-compatible event streaming between every
  pipeline stage" (purple fill)

  Row 1, right: "ParadeDB" — "Postgres 17 + pgvector + pg_search: relational data,
  embeddings, and full-text search in one database" (blue fill)

  Row 2, left: "MinIO" — "Object storage, raw archive, 90-day retention" (amber fill)

  Row 2, right: "Temporal" — "Durable cron scheduling + human-in-the-loop pause and
  resume" (blue fill)

  Row 3, left: "LiteLLM" — "Self-hosted LLM gateway: OpenAI primary, Groq automatic
  fallback" (teal fill)

  Row 3, right: "Langfuse" — "LLM call tracing and cost observability" (teal fill)

Do not draw arrows between these six nodes — they are peer infrastructure services,
not a sequential flow. Beneath the outer frame, add a small centered caption in
monospace font: "24 containerized services · 28 schema migrations · 18,755 lines of
Python · 5,250 lines of TypeScript/React".
```

---

## 5. Data Sources

| Source | Signal type | Method | Cadence | Status | Confirmed rate |
|---|---|---|---|---|---|
| NewsData.io + 10 RSS feeds | News (ET, Mint, YourStory, Inc42, Hindu BusinessLine, TechCrunch, more) | API / RSS | 5 min | 🟢 Live | 17.0% |
| Hacker News | Developer / tech discussion | API | 5 min | 🟢 Live | 32.1% |
| Jooble | Job postings — hiring signals | API | 12 h | 🟢 Live | 0%* |
| NSE | Corporate filings — capex, M&A, digital transformation | Stealth browser | 12 h | 🟢 Live | 0%* |
| BSE | Corporate filings (second exchange) | Stealth browser | 12 h | 🟢 Live | 0%* |
| GeM | Government IT procurement tenders | Stealth browser, render & scrape | 12 h | 🟢 Live | **51.9%** |
| CPPP | Government tenders (second portal) | — | — | ⏸️ Deferred | — |

\* *Jobs/filings show 0% "confirmed" not because the leads are weak, but because the
scoring rubric is still tuned for news-article language — see Section 6's calibration
note. This is the single highest-leverage near-term fix: GeM tenders already convert to
"confirmed" at **3× the rate of news** even before that fix lands.*

NSE and BSE both actively block plain scraping; GeM's search results only exist after
client-side JavaScript renders them. All three now run through a stealth browser that
mimics real user behavior. GeM search uses the public search page only — no ESDS
account or credentials are involved, so there is no risk to ESDS's registered seller
standing on the portal.

---

## 6. Scoring & Triage

Every signal gets two independent scores blended into one:

```
final_score = clip01( 0.30 × deterministic_fit + 0.70 × llm_intent_score )

confirmed:  llm.confidence == "confirmed"  AND  final_score ≥ 0.65
uncertain:  final_score ≥ 0.35
discarded:  below 0.35
```

The deterministic component is concrete facts (keyword hits, source tier, recency); the
LLM component is a genuine reading of buying intent from the full text, weighted more
heavily because intent is a judgment call, not a checklist. Scoring runs through OpenAI
(gpt-5-mini for volume, gpt-5.1 for harder calls) via a self-hosted LiteLLM gateway, with
Groq as an automatic fallback, and every call traced through Langfuse for cost control.

**Calibration note (near-term fix):** the rubric above was tuned on news-article
language. A government tender or a hiring post is a strong signal even when it doesn't
read like a news story — the fix is a source-aware weighting profile (or a manual score
floor for gov tenders) rather than one rubric for all five source types.

---

## 7. The Agentic Harness

"Agentic harness" is the code scaffold that turns a raw LLM call into a reliable,
auditable business process. An LLM by itself just answers a prompt — it has no memory of
company context, no way to fetch a website, no built-in sense of when it doesn't know
enough, and no guardrail against confidently drafting a message for a lead that isn't
actually real. The harness is everything wrapped around the model that fixes that:

| Harness responsibility | How S2R implements it |
|---|---|
| **Context assembly** | Before any LLM call, the harness gathers everything relevant — the signal, the company's known history, prior campaign attempts — into one structured "dossier" object. The model never has to guess what it knows. |
| **Tool access, scoped per stage** | The Researcher agent is the only one allowed to fetch a company website or a LinkedIn/X activity feed; the Judge and Drafter only ever see what the Researcher already collected. This keeps each LLM call cheap, fast, and focused. |
| **Structured output, not free text** | Every agent call is constrained to return a specific schema (a decision + reasoning, a dossier object, a draft with subject/body). The harness rejects and retries anything that doesn't parse — the model can't silently go off-script. |
| **A decision gate with three outcomes, not two** | Most agent pipelines force a binary "send or don't." S2R's Judge has a third option — *research more* — specifically so the model can ask for one more piece of evidence instead of guessing. This is the single biggest reason the outreach doesn't feel generic. |
| **A retry/defer loop with a hard stop** | A campaign that isn't ready yet is deferred on a recheck timer (up to 4 cycles) rather than forced into a decision — and it automatically expires rather than sitting forever. The harness enforces this; the model doesn't decide to keep trying indefinitely. |
| **A human checkpoint that cannot be skipped** | However confident the Judge is, a draft always lands in the Signal Console's review queue. The harness has no code path that sends mail without a human clicking Approve first. |
| **Full audit trail** | Every dossier, every judge decision (with its reasoning), and every send is persisted. If a message goes out, you can always answer "why did the system think this was worth sending?" |

In short: the AI does the reading, the researching, and the first draft — the same work a
skilled SDR does for every single lead — but the harness is what makes it *safe to trust
at scale*: bounded, inspectable, and never final without a human's sign-off.

---

## 8. Data Volume & Insights

### 8.1 Signal volume by source

```
NewsData.io + RSS  ██████████████████████████████████████████████████ 1,093
Hacker News         ███████████████ 318
GeM Tenders         ██ 54
Jooble (jobs)       ██ 39
NSE Filings         ▏ 1
```

### 8.2 Weekly signal volume (last 8 weeks)

```
Week of 5/11  █████████████████████████████ 192
Week of 5/18  ████████████████████████████████████████████████████████████ 391
Week of 5/25  █████████████████████ 138
Week of 6/01  ██████████████████████████ 173
Week of 6/08  ████████████████████ 133
Week of 6/15  ██████████████████████████████████ 221
Week of 6/22  ███████████████████ 121
Week of 6/29  █████████████████████ 136
```

Of 1,505 signals scored, **316 (21%) cleared the "confirmed" bar** — high-confidence
buying-intent events, not just topical mentions. The rest sit as "uncertain": lower
confidence, still visible to the team, and the exact material the planned trending page
will surface differently.

### 8.3 Where the pain is concentrated

```
Cloud migration      █████████████████████████████████████████████████ 473
Cloud cost pressure   ████████████████████████████████████████████████ 449
Security incidents    ███████████████████████████████████████████████ 442
GPU capacity           ██████████████████████████████████████ 355
Compliance              █████████████████████████ 237
Managed services         █████████████████████ 198
Data residency            ██████████████████ 172
```

```
Funding event         ██████████████████████████████████████████████████ 299
Expansion               ██████████████████████████████████ 204
Regulatory                ███████████████████████ 139
Outage                      █████████████████ 99
Hiring                        █████████████ 77
```

### 8.4 Where the companies are

```
Other                ██████████████████████████████████████████████████ 431
Enterprise             ███████████████████████████████████████████ 369
Startup                  ███████████████████████████████████ 297
Government                 █████████████████████ 184
BFSI                          ████████████████████ 173
```

Government and BFSI together already represent 357 signals — almost exactly the segment
the NSE/BSE/GeM sources were built to reach, and (per Section 5) the segment converting
to "confirmed" at the highest rate.

### 8.5 Scale of the data asset

| Metric | Value |
|---|---|
| Companies resolved & deduplicated | 2,390 |
| People identified | 2,331 |
| Competitors tracked (with 295 logged market events) | 19 |
| Deep research dossiers built | 53 |
| Outreach campaigns opened to date | 189 |
| Raw archive size | ~34 GB across ~296K objects (90-day retention policy applied) |

---

## 9. Expected Business Outcomes

**Already realized:**
- Continuous, 24/7 coverage across 7 sources that would take a full-time analyst roughly
  **75+ working days** to manually review at the same depth (1,505 signals, several
  paragraphs of judgment each) — done automatically, every day, since the platform went live.
- 189 outreach campaigns opened without a single person manually researching a company
  or drafting a first message.
- 75 personalized drafts (email + LinkedIn) sitting ready for a salesperson to simply
  review and approve — each one already researched, each one already written.
- A first real send verified end-to-end this week, proving the full loop from "signal
  detected" to "message delivered" works, not just in theory.

**Expected once the roadmap ships (Section 12):**
- **Faster time-to-contact.** Once real (non-trial) sending is live, the gap between a
  tender being posted or a filing being disclosed and ESDS's first outreach should be
  measured in **hours**, not the weeks a manual RFP-driven process currently takes.
- **Higher-quality pipeline, not just more of it.** GeM tenders already convert to
  "confirmed" 3× more often than news — as jobs/filings scoring is calibrated and more
  government/BFSI-heavy sources are added, the ratio of *real* opportunities in the
  pipeline (not just volume) should keep climbing.
- **Self-healing lead recovery.** Once monitoring agents ship (Section 12), the 31
  campaigns currently sitting "deferred, waiting for context" stop being dead ends —
  they reopen automatically the moment the company does something new, instead of
  waiting for the next full sweep.
- **A second lead motion at near-zero marginal cost.** CRM v2 reuses the exact same
  research-and-draft agent for event-attendee follow-up — meaning every ESDS-hosted or
  attended event becomes an automated, personalized outreach campaign instead of a
  spreadsheet that goes cold in a week.
- **A compounding intelligence asset.** The company/people graph (2,390 / 2,331 today)
  is not a one-time list — it grows every day the pipeline runs, and every campaign,
  every dossier, and every send is stored, making next quarter's outreach smarter than
  this quarter's by default.

---

## 10. AI's Role — Enhancing Sales & Marketing

It's worth being precise about what the AI in this platform actually replaces, because it
isn't "replacing salespeople" — it's removing the two most time-consuming, least
differentiated parts of their job so they can spend their time on the part only a human
can do: building trust and closing.

**AI system 1 — the Triage Layer.** This is the job of "someone scans the news, job
boards, and filings every morning and flags anything interesting." No analyst can
actually read 1,500+ articles, postings, and filings with real judgment every month and
still have time to do anything else. The AI does this exhaustively, instantly, and
without fatigue — and unlike a keyword alert, it's reading for *intent*, not just
mentions of "cloud" or "data center."

**AI system 2 — the Agentic Research & Drafting Layer.** This is the job of "look up this
company, find the right person, understand what's going on with them, and write a first
message that doesn't sound like a template." A skilled SDR spends 20–30 minutes doing
this well for a single contact. The Researcher/Judge/Drafter harness does it in seconds,
for every contact, every time — and unlike a mail-merge tool, every message is actually
written *from* the specific signal and the specific person's context, not from a
fill-in-the-blank template.

**What this means for the sales and marketing team in practice:**
- They stop spending time deciding *which* of hundreds of possible leads to chase first —
  the platform has already read everything and ranked it.
- They stop starting from a blank page — every approved draft already reflects real
  research on the company and the person.
- Their working set shrinks to exactly the decisions that require human judgment:
  *does this draft sound right, is this the right moment, should I personalize this
  line further* — and then a single click to send.
- The team's reach scales with the number of signals the platform can process, not with
  headcount — the same effect email automation had on marketing throughput two decades
  ago, applied to the harder, more personal work of signal-based sales outreach.

The strategic bet here is straightforward: the companies that win the next wave of B2B
selling won't be the ones with the biggest SDR teams — they'll be the ones whose AI reads
everything, so their humans only have to act on what actually matters.

---

## 11. Build Timeline

| Phases | Milestone |
|---|---|
| 01–04 | Foundation, storage, streaming, orchestration — the substrate everything else runs on |
| 05–10 | First pipeline: news, HN, crawler, filter/dedup, triage, persistence (original 2-source POC) |
| 11–17 | Verification UI, bug-fix hardening, entity resolution, observability, E2E tests |
| **18–21** | **Competitor monitoring + agentic outreach foundation** — first version of research → draft → review → send |
| 22–24 | Lean-stack cleanup, Signal Console launch, OpenAI migration + Langfuse tracing + Apollo |
| **25** | **Agentic research → personalized outreach** — the researcher/judge/drafter loop, live |
| 27 | Pipeline refinement — company-level campaigns (one live thread per company), 3-queue review model |
| **28–29** | **Stealth-fetch fallback + 4 new data sources** — Camoufox bypass, Jooble/NSE/BSE/GeM ingestors |
| — | S2R rebrand — customer-facing product shell, per-user authentication |
| — | Live SMTP send verified end-to-end (this week) |

---

## 12. Roadmap

| Priority | Item | Detail |
|---|---|---|
| **Highest** | **CRM v2 — event-driven warm outreach** | Upload an event attendee sheet; the same research/draft agent runs per attendee, grouped by company, with full audit history. Build-ready. |
| High | **Real email go-live** | Sender is built and tested. Needs the on-prem Exchange SMTP host confirmed + SMTP-AUTH enabled for insight@esds.co.in — then it's a one-line config flip, no code change. |
| High | **Reply-handling design** | What happens when a prospect replies to insight@ — routing to BDM@esds.co.in and the rep team is not yet designed. |
| High | **Source-aware scoring calibration** | Fix the news-tuned rubric so jobs/tenders/filings score on their own merits (Section 6). |
| Medium | **Monitoring agents** (watchlist) | Scheduled re-checks on deferred/research-more campaigns so a stale lead reopens itself. |
| Medium | **Apollo enrichment confirmation** | Confirm API key + credit budget are active — several demo drafts are missing contact emails, which is Apollo's job to fill. |
| Deferred | **CPPP — second tender portal** | Session handling is more involved than GeM's; scoped as dedicated follow-up so it doesn't block the sources already shipped. |
| In design | **Trending / leaderboard view** | Same pipeline, looser keyword gate, surfaces what's rising rather than only what clears the buying-intent bar. |
| In design | **Reddit / Quora / X person-first pipeline** | Individuals voicing technical pain, or a competitor's own customers complaining publicly. |
| In design | **MCP tool server** | Gives agents a standard tool-calling interface instead of hand-wired integrations. |
| Later | **Temporal migration for outreach worker** | Move off the poll-based sweeper — locked decision to do this *after* monitoring agents ship. |
| Later | **Storage volume provisioning** | 90-day retention is live; still deciding on a dedicated volume size (~250 GB suggested) for long-term headroom. |

---

## 13. Closing

Every service, every scraper, every line of the scoring logic, the agentic outreach loop,
and both the internal console and the S2R product shell were designed and built end to
end, solo, from a blank repository to a running seven-source intelligence platform with
a live, human-approved outreach loop already sending real mail.

*S2R — Signal to Response · ESDS Software Solutions · Internal report*
