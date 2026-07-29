# S2R — Signal to Response
### Platform Status & Roadmap Report

**Prepared by:** Sahil Sahu (sahil.sahu@esds.co.in)
**Date:** 1 July 2026
**Scope:** Phases 01–29, built solo, end to end

---

## 1. Executive Summary

S2R watches the public internet — news, developer chatter, job postings, stock-exchange
filings, government tenders — for signs that an Indian enterprise is under IT pain ESDS
can solve. It scores buying intent with LLMs, tracks the company and people behind every
signal, and is now drafting the outreach that turns a signal into a conversation.

| Metric | Value |
|---|---|
| Signals scored to date | **1,454** |
| Companies tracked | **2,268** |
| Contacts identified | **2,256** |
| Live data sources | **7** (4 added this cycle) |
| Outreach campaigns opened | **188** |
| Personalized drafts awaiting review | **76** |

Everything described in this report — the architecture, the 24 running services, the
scraping engineering needed to get past exchange and government anti-bot defenses, the
LLM-driven research-and-draft agent, and the customer-facing product shell — was designed
and built end to end by one person, with no external team or outsourced component.

---

## 2. What S2R Does

Cloud migrations, security incidents, funding rounds, compliance deadlines, GPU capacity
crunches — these events are announced publicly, in fragments, across dozens of sources,
long before a company issues an RFP. S2R's job is to catch those fragments early, decide
which ones represent a real buying signal for ESDS's cloud, data-center, and
managed-services catalog, and put the right person's name and contact in front of the
sales team before a competitor does — or draft the first message itself.

The platform is deliberately built as an assembly line, not a single script: every
stage — fetch, clean, filter, score, decide, act — is its own service, so a bad day on
one source (a blocked scraper, a bad API response) never stalls the rest of the pipeline.

---

## 3. Architecture

Every source has its own ingestor. Ingestors archive raw data to object storage first
(nothing is ever lost even if downstream logic changes), then publish an event. A shared
crawler fetches full article bodies, falling back to a stealth browser when a site blocks
plain HTTP. A filter/dedup stage removes noise and near-duplicates using both fingerprint
hashing and semantic (vector) similarity. An LLM triage stage scores buying intent. From
there, signals either land in the human-facing console, or — if they clear the bar — open
an autonomous research-and-outreach campaign.

### Core signal pipeline

```
7× Ingestors → MinIO raw archive → Redpanda topic → Crawler (+ Camoufox stealth fallback)
   → Filter / Dedup (MinHash + pgvector) → LLM Triage (hybrid score) → Persistence
   → Signal Console
```

### Infrastructure layer — fully self-hosted

| Component | Role |
|---|---|
| Redpanda | Kafka-compatible event streaming between every pipeline stage |
| ParadeDB | Postgres 17 + pgvector + pg_search — relational data, embeddings, and full-text search in one database |
| MinIO | Object storage — every raw payload archived before any processing, replayable |
| Temporal | Durable cron scheduling and human-in-the-loop pause/resume |
| LiteLLM | Self-hosted LLM gateway — OpenAI primary, Groq fallback, full cost control |
| Langfuse | LLM call tracing and cost observability |

### Codebase scale

| Metric | Value |
|---|---|
| Containerized services | 24 |
| Database schema migrations | 28 |
| Lines of Python (services + libs) | 18,755 |
| Lines of TypeScript/React (console UI) | 5,250 |
| Automated test files | 41 |

---

## 4. Data Sources

The platform started on news + Hacker News. This cycle added three categories that speak
directly to buying intent that news coverage misses entirely: hiring (a company staffing
up for cloud/security roles is telling you something), regulatory filings (an acquisition
or capex disclosure), and government procurement (a live tender is the single strongest
signal there is — the money is already budgeted).

| Source | Signal type | Method | Cadence | Status |
|---|---|---|---|---|
| NewsData.io + 10 RSS feeds | News (ET, Mint, YourStory, Inc42, Hindu BusinessLine, TechCrunch, more) | API / RSS | 5 min | 🟢 Live |
| Hacker News | Developer / tech discussion | API | 5 min | 🟢 Live |
| Jooble | Job postings — hiring signals | API | 12 h | 🟢 Live |
| NSE | Corporate filings — capex, M&A, digital transformation | Stealth browser fetch | 12 h | 🟢 Live |
| BSE | Corporate filings (second exchange) | Stealth browser fetch | 12 h | 🟢 Live |
| GeM | Government IT procurement tenders | Stealth browser, render & scrape | 12 h | 🟢 Live |
| CPPP | Government tenders (second portal) | — | — | ⏸ Deferred |

**Note on scraping:** NSE and BSE both actively block plain scraping (HTTP 403 / JS-only
rendering). Both now run through a stealth browser that mimics real user behavior. GeM
tenders required a full rewrite: the portal's search results only exist after
client-side JavaScript renders them — the old approach was reading an empty page
template. Search uses GeM's public search only; no ESDS account or credentials are
involved, so there is no risk to ESDS's registered seller standing on the portal.

---

## 5. Scoring & Triage

Every signal gets two independent scores that are blended: a deterministic score from
concrete facts (keyword hits, source tier, recency), and an LLM's read of actual buying
intent from the full text. The LLM component is weighted more heavily — intent is a
judgment call, not a checklist.

```
final_score = clip01( 0.30 × deterministic_fit + 0.70 × llm_intent_score )
```

- **Confirmed** requires both an LLM confidence of "confirmed" AND a final score ≥ 0.65
- **Uncertain** requires a final score ≥ 0.35
- Below that: discarded

Scoring is powered by OpenAI (gpt-5-mini for volume, gpt-5.1 for harder judgment calls)
through the self-hosted LiteLLM gateway, with Groq as an automatic fallback if OpenAI is
unavailable. Every call is traced through Langfuse for cost and quality monitoring.

---

## 6. Agentic Research & Automated Outreach

A confirmed signal doesn't just sit in a dashboard. If the company matches ESDS's target
roster (or clears a high-confidence bar as a prospect) and isn't already excluded, an
autonomous campaign opens automatically — one live campaign per company, so five signals
about the same company fold into one thread instead of five.

### Agentic outreach flow

```
Confirmed signal → Outreach Gate (roster + timing rules) → Contact Resolution
   (existing contacts → Apollo enrichment) → Researcher (company site + LinkedIn/X
   activity) → Judge (LLM decision)
```

The Judge decides one of three outcomes for every campaign:

- **Draft** — enough signal to write a personalized email + LinkedIn message per
  contact. Drafts land in a human review queue in the Signal Console; nothing sends
  without approval.
- **Research more** — one more targeted research pass (company website, contact's
  recent LinkedIn activity), then the Judge re-decides.
- **Defer** — not enough context yet. Rechecked automatically on a timer (up to 4
  cycles) before the campaign expires.

Approved drafts go out through the sender service, which currently routes every send to
a trial inbox for QA — flip one setting once contact enrichment (Apollo) and sign-off are
complete, and the same code path sends to the real prospect from **insight@esds.co.in**
on ESDS's own mail server.

| Metric | Value |
|---|---|
| Campaigns opened | 188 |
| In human review right now | 11 |
| Drafts ready for approval (38 email + 38 LinkedIn) | 76 |
| Deferred, waiting for a fresh hook | 30 |

### Monitoring agents — designed, next to build

Deferred and "research more" campaigns currently only get re-checked when the sweeper
revisits them. The next step is a dedicated **watchlist**: a small, targeted list of
companies-in-waiting, each re-checked by a Temporal-scheduled monitoring agent at its own
cadence — pulling fresh LinkedIn/X activity and company news — without re-scanning the
whole database. This is what turns "we drafted something six weeks ago and it went
stale" into "we noticed they just posted about a new data center and re-opened the
conversation."

---

## 7. Data Volume & Insights

Of the 1,454 signals scored, 304 (21%) cleared the "confirmed" bar — high-confidence
buying-intent events, not just topical mentions. The rest sit as "uncertain": lower
confidence, but still visible to the team and available for the trending/monitoring work
planned next.

### Signals scored per week (last 8 weeks)

| Week of | Signals |
|---|---|
| 5/11 | 192 |
| 5/18 | 391 |
| 5/25 | 138 |
| 6/01 | 173 |
| 6/08 | 133 |
| 6/15 | 221 |
| 6/22 | 121 |
| 6/29* | 85 |

*Week of 6/29 is partial — the 4 new sources only started producing signals on 7/1, not
yet reflected in this trend.

### Where the pain is concentrated

| Pain category | Signals | Event type | Signals |
|---|---|---|---|
| Cloud migration | 469 | Funding | 287 |
| Cloud cost pressure | 448 | Expansion | 195 |
| Security incidents | 440 | Regulatory | 136 |
| GPU capacity | 344 | Outage | 99 |
| Compliance | 231 | Hiring | 72 |

Enterprise and BFSI together account for a third of all tracked signals, with Government
close behind at 159 — exactly the segment the new NSE/BSE/GeM sources were built to
reach.

### Scale in the database and archive

| Metric | Value |
|---|---|
| Companies resolved & deduped | 2,268 |
| People identified | 2,256 |
| Competitors tracked (285 events) | 19 |
| Deep research dossiers built | 52 |
| Raw archive size | ~34 GB across ~296K objects (90-day retention policy) |

---

## 8. Build Timeline

Each phase shipped in order — foundation and plumbing first, intelligence next, then
agentic behavior on top.

| Phases | Milestone | Notes |
|---|---|---|
| 01–04 | Foundation, storage, streaming, orchestration | uv monorepo, ParadeDB, Redpanda, Temporal — the substrate everything else runs on |
| 05–10 | First pipeline: news, HN, crawler, filter/dedup, triage, persistence | The original two-source proof of concept, end to end |
| 11–17 | Verification UI, bug-fix hardening, entity resolution, observability, E2E tests | |
| **18–21** | **Competitor monitoring + agentic outreach foundation** | First version of research → draft → review → send |
| 22–24 | Lean-stack cleanup, Signal Console launch, OpenAI migration | Business-facing UI on :8502; OpenAI primary + Langfuse tracing + Apollo integration |
| **25** | **Agentic research → personalized outreach** | The researcher/judge/drafter loop described in Section 6 — built and live |
| 27 | Pipeline refinement | Company-level campaigns (one live thread per company), 3-queue review model, bulk dedup of duplicate entities |
| **28–29** | **Stealth-fetch fallback + 4 new data sources** | Camoufox browser bypass, Jooble/NSE/BSE/GeM ingestors — this report's headline work |
| — | S2R rebrand — customer-facing product shell | New login/signup, per-user authentication, product identity separate from the internal ops console |

---

## 9. This Cycle's Operational Work

New data sources exposed problems that had been silently dormant in the shared
pipeline. None were visible until real job/tender/filing data started flowing through
it. Diagnosed and fixed in a single session, in order of discovery:

1. **Silent data loss on every job posting** — a timezone bug crashed the filter stage
   on every single job record — 100% loss, no error visible upstream. Fixed at the
   source and at the choke point.
2. **Double-filtering pre-qualified sources** — jobs/tenders/filings were being run
   through a news-tuned keyword filter meant for a different kind of source, discarding
   legitimate items.
3. **Stale service build rejecting new source types** — the scoring service was running
   an old build that didn't know the 3 new source types existed.
4. **Database crash on company records with no website** — every job/tender/filing has
   no company domain by definition — an edge case the persistence layer had never hit
   before.
5. **Exchange & government portals actively blocking scraping** — NSE returned 403 to
   every request; GeM's results only exist after JavaScript renders them. Both rebuilt
   on a stealth browser.
6. **Server disk full, blocking all new data** — accumulated build artifacts filled the
   disk to 100%, silently rejecting every new write. Freed and a 90-day
   archive-retention policy added so it can't recur.

**Also shipped this cycle:** a live Source Health panel in the console — every scraper
now reports ok / blocked / error after each run, so a future anti-bot change on NSE,
BSE, or GeM surfaces as a visible alert instead of silent data loss; and a second
exchange (BSE) and a fully rewritten GeM scraper going from 1 fake placeholder tender to
56 real ones per run.

---

## 10. Roadmap

| Priority | Item | Description |
|---|---|---|
| **Highest** | CRM v2 — event-driven warm outreach | Upload an event attendee sheet (conference, ESDS-hosted event) and the same research/draft agent runs against every attendee, grouped by company, with full audit history and an editable review step before anything locks and sends. Build-ready. |
| In design | Monitoring agents (watchlist) | Scheduled re-checks on deferred / research-more campaigns so a stale lead reopens itself when the company does something new, instead of waiting for the next full sweep. |
| Deferred | CPPP — second government tender portal | Session handling is more involved than GeM's; scoped as dedicated follow-up work so it doesn't block the other three sources shipped this cycle. |
| In design | Trending / leaderboard view | Same pipeline, a looser keyword configuration, surfacing what's rising in volume rather than only what clears the buying-intent bar. |
| In design | Reddit / Quora / X person-first pipeline | Individuals voicing technical pain, or a competitor's own customers complaining publicly — a lead source no competitor is watching. |
| Near-term fix | Source-aware scoring calibration | The scoring rubric was tuned on news article language. A government IT tender is a strong signal by itself even when it doesn't read like a news story — jobs/tenders/filings need their own calibration so a real tender doesn't score lower than a news mention. |
| Pending access | Live email send | Sender is built and tested in trial mode. Going live needs the Exchange SMTP host confirmed and authenticated-SMTP enabled for insight@esds.co.in — then it's a one-line config flip, no code change. |

---

## Closing Note

Every service, every scraper, every line of the scoring logic, the agentic outreach
loop, and both the internal console and the S2R product shell — designed and built end
to end, solo, from a blank repository to a running seven-source intelligence platform.

*S2R — Signal to Response · ESDS Software Solutions · Internal report*
