# Ask Kochi Engineering Plan

> **Roadmap status (verified 2026-07-18):** Ask Kochi is at project zero. The
> repository contains only `agents.md`, `skills.md`, `plan.md`, an empty `README.md`,
> a license, and a project image (plus local OS metadata). Product code, datasets,
> tests, infrastructure, runtime configuration, CI, and the frontend do not exist.
> A path or technology described below is proposed until an approved milestone creates
> and verifies it.

## Purpose and delivery standard

Ask Kochi is an AI-powered local-city companion for residents and visitors to Kochi, Kerala. It converts natural-language questions—such as where to eat near Fort Kochi, which metro stop to use, or what to do in rain—into grounded, useful, and safe answers. The product must prefer verified local data and live tool results over plausible language-model guesses.

This plan is the implementation sequence and decision record for agents working in this repository. Work in the order below unless a task explicitly depends on an earlier missing capability. A feature is incomplete until its tests, observability, privacy implications, dataset/indexing impact, and documentation have been considered.

## Current repository baseline

**Verified:** no product directories or executable project configuration exist. In
particular, there is no `backend/`, `frontend/`, `datasets/`, `schemas/`, test suite,
package/dependency manifest, compose configuration, CI workflow, or `.env.example`.
There are no application routes, SSE events, persistence models, index collections,
provider defaults, or developer commands to preserve.

**Proposed:** FastAPI, PostgreSQL, Redis, Qdrant, Firebase-compatible auth, indexing,
SSE, and a React PWA are the target architecture, subject to M0 contract and provider
decisions. Treat inspected code and committed contracts as the source of truth when
they differ from this plan. Update this section after each milestone establishes a
verified capability.

## Engineering principles

1. Ship a working, demoable vertical slice before expanding breadth.
2. Prefer deterministic systems: schema-validated data, typed boundaries, stable IDs, bounded retries, and explicit versions.
3. Define the contract before crossing a service, data, tool, or UI boundary.
4. Preserve source identity, freshness, and uncertainty through retrieval and citations.
5. Measure before optimizing; never optimize speculative bottlenecks or reduce grounding to improve a metric.
6. Keep modules small, compose focused components, and avoid duplicate business policy.
7. Fail safely and transparently when live data, evidence, location, or a dependency is unavailable.
8. Use mature libraries and the smallest practical surface area for the hackathon.

## Expected repository layout and ownership

This is the target layout, not a checklist of directories to create upfront. The first named owner owns the slice; required partners review the listed boundary.

| Path | Purpose | Owner / required partner |
| --- | --- | --- |
| `backend/app/routers/` | Thin FastAPI HTTP and SSE contracts. | Backend / Testing, Security |
| `backend/app/services/`, `models/`, `dependencies/`, `middleware/`, `settings.*` | Business services, persistence, request lifecycle, typed configuration. | Backend / Security; DevOps for deployment config |
| `backend/app/rag/`, `backend/indexing/` | Retrieval runtime and deterministic JSON-to-Qdrant ingestion. | RAG / Dataset, Validation, AI |
| `backend/app/prompts/`, `backend/app/tools/` | Versioned LLM prompts and typed live-tool adapters. | AI / RAG, Security, Geo |
| `backend/app/geo/` | WGS84 validation, distance and route contracts. | Geo / Frontend, Security |
| `backend/tests/`, `tests/` | Backend and cross-service regression evidence. | Testing / affected owner |
| `frontend/src/` | React, TypeScript, Tailwind, PWA, typed API/SSE client. | Frontend / Backend, Geo, Testing |
| `datasets/` and `schemas/` | Curated JSON source of truth and schema registry. | Dataset / Validation, RAG |
| `scripts/` | Deterministic validation and operational utilities. | RAG / Validation, DevOps |
| `docker/`, `docker-compose.yml`, `.github/workflows/` | Local topology, CI, deployment automation. | DevOps / Backend, Security |
| `docs/`, `README.md`, `agents.md`, `skills.md`, `plan.md` | Current-state setup, standards, contracts, runbooks, decisions. | Documentation / affected owner |

## Demo priorities and explicit non-goals

| Priority | Capability | Demo standard |
| --- | --- | --- |
| Critical | Chat with cited local answers | A user can ask, see streamed grounded text, and open/understand each source. |
| Critical | Restaurants, weather, metro, maps, nearby search, emergency information | Each works through the typed policy path and fails transparently when evidence/live data is unavailable. |
| Secondary | Offline shell, events, analytics, voice | Add only after all demo-critical journeys work end-to-end. |
| Not in hackathon scope | Payments/bookings, plugin marketplace, admin dashboard, broad multilingual support | Do not create partial versions without an explicit product decision. |

**First vertical slice (proposed):** one read-only, cited local-place question with a
transparent empty-evidence fallback. It establishes the smallest end-to-end contract
before weather, metro, maps, nearby search, emergency information, authentication,
or broad UI work. Do not represent any of those later capabilities as available until
their contracts and tests exist.

## Milestone dependency graph

Agents must not skip a dependency unless the task owner records why the prerequisite is unnecessary and verifies no contract is bypassed.

```text
M0: runnable, observable foundation
 └── M1: validated, sourceable datasets
      └── M2: versioned indexing and evaluated retrieval
           └── M3: grounded conversation and live-tool orchestration
                └── M4: customer PWA over stable API/SSE contracts
M5: secure operation, CI, deployment, and scale controls (depends on M0–M4)
```

## Cross-milestone service-level targets

These are practical hackathon budgets measured locally with dependencies warmed and reported with sample size, p50, and p95. A missed target blocks demo-critical expansion only when it makes the user journey unreliable; otherwise record the limitation and mitigation.

| Surface | Target | Measurement boundary |
| --- | --- | --- |
| Health/readiness endpoint | p95 < 100 ms | API process to response, dependencies healthy |
| Dataset validation | < 30 s | Full curated corpus in CI/local reference fixture |
| Retrieval (embedding excluded) | p95 < 150 ms | retriever request to ranked payloads |
| Embedding + retrieval | p95 < 800 ms | cached/local provider path; report external variance separately |
| Live weather/tool adapter | p95 < 2 s; timeout <= 3 s | adapter request to normalized result/fallback |
| First streamed token | p95 < 1.5 s after context is ready | LLM call to first `message` event |
| Chat orchestration after retrieval | p95 < 500 ms excluding LLM generation | policy/context/persistence path |
| Frontend initial JS | < 250 KB gzip for demo route | production build analyzer |
| Core interaction | cited answer success >= 95% in scripted demo runs | 20-run smoke suite; dependency failures disclosed |

## Definition of Ready

Do not begin implementation until the work item records the following. An agent must stop and request a decision when a missing item would change a public contract, source of truth, authorization boundary, migration/index operation, or demo behavior.

- User outcome, acceptance criteria, required milestone, owner, and partners.
- Dependencies and a confirmed dependency-graph position.
- Typed API/SSE, schema, tool, or UI interface; compatibility/versioning expectation.
- Required dataset/source provenance and freshness expectations, or an explicit statement that no data changes.
- Verification plan: deterministic tests, manual demo path, performance metric if user-facing, and negative/timeout cases.
- Security/privacy posture, configuration changes, observability, rollout, rollback, and stated non-goals.

## Definition of Done

A feature is complete only when the agreed acceptance criteria are observable; implementation and relevant unit, integration, regression, negative, permission, and timeout tests pass; schema/dataset validation and index impact are addressed; logs/metrics are present at the affected boundary; documentation/configuration/migration notes are current; stateful changes have a tested rollback path; and no critical TODO or unrecorded dependency remains. Report exact commands and results in the handoff.

## Target architecture

```text
PWA (React, TypeScript, Tailwind, Leaflet)
  -> FastAPI API / SSE chat
  -> intent classification and request policy
  -> live-tool selection + retrieval orchestration
  -> Redis cache | PostgreSQL sessions/analytics | Qdrant knowledge base
  -> response grounding, citations, formatting, safety checks
  -> user
```

When created, the backend will be the authority for authentication, tool credentials,
query policy, retrieval, LLM calls, citations, and persistence. The client must never
receive secrets, database credentials, Firebase admin credentials, or raw internal
prompts.

## Milestones

### M0 — Stabilize the foundation

**Depends on:** none. **Primary owner:** Backend. **Required partners:** Testing and Security; DevOps for local topology. **Unlocks:** M1–M5.

1. Preserve this zero-state baseline in the plan before creating product files. Decide and document the first vertical slice, its public contract, provider/auth posture, and non-goals; do not assume a route, event name, or provider default already exists.
2. Create only the minimal runnable application, dependency manifest, formatting/lint/test configuration, and developer commands required for that slice. Add an accurate README setup path at the same time.
3. Establish typed contracts for health/readiness and the first read-only answer path. If sessions or streaming are included, define their versioned ownership and event contracts before implementation; otherwise explicitly defer them.
4. Add typed settings, safe structured logs/request IDs, explicit timeouts, CORS policy, and graceful dependency failures proportionate to the first slice. Add `.env.example` only for configuration that is actually introduced, never credentials.
5. Introduce persistence, Redis, Qdrant, migrations, live providers, and authentication only when the first slice needs them. PostgreSQL is the intended deployed database once persistence is introduced; SQLite may support isolated compatible tests.

**Deliverables:** a runnable minimal service; declared toolchain and developer commands; typed health/readiness and first-answer contracts; a documented decision on session/SSE scope; safe settings/logging/error behavior; focused startup/route tests; an accurate README; and a smoke-test report. Add databases, containers, migrations, and provider adapters only when they are justified by this slice.

**Success metrics:** a clean clone completes the documented setup and smoke path; the first-answer path returns either an attributed result or an explicit safe fallback; health/readiness p95 is under 100 ms when implemented; all introduced tests/lint pass; invalid input and dependency-failure paths pass; session ownership and SSE event-order tests pass if those features are introduced; no secret scanner finding is introduced.

**Validation:** run only commands created and documented by M0—for example, the configured formatter/linter, test suite, startup smoke, and first-answer HTTP smoke. Add container, migration, indexing, session, or SSE smoke commands only if their corresponding component is introduced; document each target's exact behavior before claiming it passed.

**Rollback/state:** revert the deployment; downgrade only the new, reviewed Alembic revision on disposable/local environments; retain a documented database backup procedure before any shared-environment migration.

**Not included by default:** full provider integrations, persistence, authentication, production deployment, frontend, broad datasets, retrieval tuning, or any infrastructure not required by the first slice.

**Exit criteria:** a clean clone can follow verified setup instructions, start the minimal service, call its documented health endpoint, and complete the first read-only answer path with a safe fallback. Any added session, streaming, data, database, or index component has a typed contract and focused tests; no secret files are committed.

### M1 — Make knowledge data trustworthy

**Depends on:** M0. **Primary owner:** Dataset. **Required partners:** Validation and RAG. **Unlocks:** M2–M5 curated-data work.

1. Inventory every JSON dataset under `datasets/` and associate it with a schema or an explicit task-specific schema.
2. Implement a validation command that verifies JSON syntax, top-level array shape, required fields, ID uniqueness, type consistency, coordinate ranges, known categories, URL/phone formatting where present, timestamps, duplicate records, and broken cross-references.
3. Require provenance (`source`), `last_verified`, and `estimated` where the canonical schema expects them. Mark unknown facts rather than inventing them.
4. Create deterministic IDs and normalized category names. Keep source JSON readable; do not replace it with generated prose.
5. Emit a machine-readable validation report and fail CI for schema errors or duplicate IDs.

**Deliverables:** `datasets/` inventory; canonical and task-specific schemas; deterministic validator and machine-readable report; valid demo-critical records with provenance; duplicate/reference/coordinate fixtures; CI validation step; dataset contribution and source-freshness documentation.

**Success metrics:** 100% of committed dataset records pass schema and semantic validation; every report error names file, record index, JSON path, and rule; duplicate-ID and invalid-coordinate fixtures fail deterministically; validation completes within 30 seconds; each demo-critical record includes source and `last_verified` when the schema requires it.

**Validation:** run the validator on the full corpus and invalid fixtures; review source/date for each demo-critical record; demonstrate that one controlled dataset edit changes exactly the expected document hash/input in the indexing dry run.

**Rollback/state:** restore the prior version-controlled JSON/schema commit, rerun validation, and schedule a re-index; do not patch Qdrant directly to compensate for source JSON.

**Not included:** scraping at scale, generated factual content, a general CMS, or unsupported claims presented as verified.

**Exit criteria:** all datasets validate, validation reports identify file and record path, and a dataset edit deterministically changes the relevant index documents.

### M2 — Production-grade indexing and retrieval

**Depends on:** M1. **Primary owner:** RAG. **Required partners:** Dataset, Validation, AI, and Testing. **Unlocks:** M3 and cited frontend answers in M4.

1. Build documents from JSON with title, normalized content, stable parent ID, category, source file, latitude, longitude, tags, freshness fields, and raw source reference.
2. Chunk long documents at semantic boundaries, target 500–1000 tokens, and overlap up to 100 tokens. Do not split JSON tokens, coordinates, phone numbers, URLs, or source attribution.
3. Version the collection by embedding model and document schema. Store content hash and index timestamp so unchanged chunks are not re-embedded.
4. Upsert Qdrant points idempotently; delete or mark stale points for records removed from the source dataset.
5. Retrieve with vector similarity plus category filters, optional metadata constraints, and geo filtering. Add hybrid lexical search only when it is measured to improve the evaluation set.
6. Rerank the bounded candidate set using a deterministic local or hosted ranker. Preserve original retrieval score and reranker score for debugging.

**Deliverables:** deterministic document/chunk builder; versioned Qdrant collection naming and payload schema; content-hash incremental indexer; stale-record policy; retrieval/reranking API; fixed offline evaluation set with expected source IDs; relevance and index-run reports; index operation runbook.

**Success metrics:** a second unchanged indexing run performs zero re-embeds and yields the same point IDs/count; 100% of returned citations resolve to a source record or normalized live payload; Recall@10 is at least 0.80 across the fixed demo-critical evaluation set, with no critical-query regression from its approved baseline; retrieval p95 is below 150 ms excluding embedding.

**Validation:** run index twice against a disposable versioned collection; run the evaluation set before and after retrieval changes; assert payload identity, stale-record handling, category/geo filters, empty results, and citation resolution; publish the model, schema, corpus commit, and score report together.

**Rollback/state:** retain the prior collection alias/version and corpus commit; switch the application back to that alias on regression; never mix embedding-model dimensions in one collection.

**Not included:** hybrid/lexical retrieval unless its evaluation improves the fixed set, online learning, or unbounded corpus ingestion.

**Exit criteria:** indexing can run twice safely, retrieval has offline relevance tests, and every answer citation resolves to a dataset record or live tool payload.

### M3 — Conversation and tool orchestration

**Depends on:** M2. **Primary owner:** AI. **Required partners:** RAG, Backend, Geo, Security, and Testing. **Unlocks:** M4 chat experience and M5 production controls.

1. Define a structured intent result: `intent`, `confidence`, `requires_live_data`, `required_location`, `allowed_tools`, and `clarifying_question`.
2. Replace keyword-only routing incrementally with policy-gated tool calling. Tools include weather, nearby search, directions/distance via OSRM, events, metro route, emergency contacts, and hospital lookup.
3. Validate tool parameters server-side; set timeouts, retry only safe idempotent reads, cache short-lived results, and gracefully disclose unavailable tools.
4. Retrieve domain knowledge even when a live tool runs, unless the request is intentionally live-only. Live facts win for time-sensitive data; cite both when both materially inform the answer.
5. Assemble context with source labels, freshness, and strict size budgets. Instruct the LLM to use only provided facts, distinguish estimates, and ask a brief clarification when needed.
6. Stream `meta`, `message`, `error`, and `done` SSE events with a versioned event contract.

**Deliverables:** versioned intent and tool-policy schemas; normalized typed adapters for the demo-critical live tools; versioned prompts/context assembler; versioned `meta`/`message`/`error`/`done` SSE specification; tool/cache configuration; evaluation fixtures; injection, timeout, stale-data, and missing-location tests; response/citation observability.

**Success metrics:** 100% of scripted factual answers include resolvable citations or an explicit abstention; at least 95% of the fixed critical-answer evaluation set is grounded or safely abstains; all tool calls obey a <=3-second timeout and return a safe fallback on dependency failure; first streamed token is p95 <1.5 seconds after context is ready; no fixture can cause tool/retrieved text to change system policy.

**Validation:** execute the evaluation scenarios named in the exit criteria plus malformed-tool-output, prompt-injection, cancellation, and event-order tests; capture tool/retrieval/LLM latency and citation-rate report; manually run the demo-critical tool paths using controlled provider fakes before live credentials.

**Rollback/state:** disable the affected tool through explicit configuration/feature flag, deploy the prior prompt/policy version, and keep retrieval-only answers or transparent unavailability; do not silently substitute stale live facts.

**Not included:** autonomous actions, unreviewed tools, broad general-chat support, or long-term memory beyond the approved session policy.

**Exit criteria:** evaluations cover food, transport, weather, emergency, off-topic, missing-location, and stale-data scenarios; no tool output is treated as trusted instructions.

### M4 — Build the customer frontend

**Depends on:** M3 (and M0 API/SSE contracts). **Primary owner:** Frontend. **Required partners:** Backend, Geo, and Testing. **Unlocks:** customer demo and production UI rollout in M5.

1. Create a Vite + React + TypeScript application with Tailwind, typed API client, routing, and PWA manifest/service worker.
2. Deliver chat, streaming message rendering, citations, suggested questions, location permission controls, retry states, session list, and accessible keyboard behavior.
3. Use Leaflet and OpenStreetMap for maps. Render map pins only from validated coordinates; use OSRM results for routes rather than calculating road distance client-side.
4. Keep the app responsive from 320px mobile through desktop. Respect reduced motion, focus management, contrast, semantic headings, and touch target sizing.
5. Cache static shell assets for offline use; never imply that time-sensitive content is current while offline.

**Deliverables:** Vite/React/TypeScript/Tailwind app; strict typed API and SSE client; chat/citation/map/location/session UI; PWA manifest and static-shell cache; accessibility and responsive tests; error/reconnect/offline states; production build report; screenshot-based demo checklist.

**Success metrics:** all demo-critical journeys complete at 320px and desktop with keyboard-only navigation; Lighthouse accessibility score is >=90 on the chat route (or documented equivalent automated check); production initial JavaScript is <250 KB gzip for the demo route; SSE reconnect and malformed-citation tests pass; a denied-location user can still search by named/manual location.

**Validation:** run typecheck, lint, unit/component tests, production build/bundle analysis, keyboard walkthrough, viewport checks at 320px and desktop, and scripted SSE disconnect/reconnect/offline-live-data scenarios.

**Rollback/state:** deploy the prior static artifact or disable the new UI behind a frontend feature flag; retain the last compatible version of the API/SSE client during backend rollout.

**Not included:** native applications, voice input, payment/booking, analytics dashboards, or broad offline live-data claims.

**Exit criteria:** Lighthouse/accessibility checks are acceptable for the project target, SSE reconnection is tested, and the PWA safely explains unavailable live features.

### M5 — Operate securely and scale deliberately

**Depends on:** M0–M4. **Primary owner:** DevOps. **Required partners:** Backend, Security, RAG, and Testing. **Unlocks:** repeatable demo/production deployment.

1. Add authentication policy, per-user/IP rate limits, abuse controls, audit-safe structured logs, error tracking, metrics, and alerting.
2. Cache embeddings by normalized query/model, retrieval results by query/filter/index version, and tool results according to source freshness. Never cache private session content across users.
3. Add GitHub Actions for lint, tests, dataset validation, index smoke tests, dependency audit, and container build.
4. Deploy stateless API replicas behind TLS; keep Qdrant, Redis, and PostgreSQL managed/persistent with backups and migration rollout rules.
5. Establish quality dashboards: latency, cache hit rate, tool error rate, answer citation rate, grounded-answer pass rate, retrieval relevance, and dataset freshness.

**Deliverables:** CI workflows; container build; environment/secrets reference; deployment topology and health checks; migration/index rollout scripts; dashboard/alert definitions; backup/restore and rollback runbooks; rate-limit/cache configuration; dependency-audit evidence; release smoke script.

**Success metrics:** a clean CI run executes lint, tests, dataset validation, index smoke, audit, and container build; every deployment emits a release/version marker and passes health/readiness smoke checks; 100% of state-changing releases name a backup and rollback action; dashboard reports p50/p95 endpoint, retrieval, tool, LLM, cache, citation, and freshness metrics; no production secret is present in source, image layers, or logs.

**Validation:** execute a clean environment deploy rehearsal, migration on a blank database, disposable collection rebuild, rollback rehearsal, restore test, dependency audit, and failure-mode smoke tests for an unavailable Qdrant/Redis/provider.

**Rollback/state:** use the ordered rollback plan below: stop traffic, roll back application/frontend artifacts, restore the prior index alias and compatible dataset, then run only the reviewed migration downgrade/restore procedure. Never roll back a destructive migration or collection rebuild without a verified backup.

**Not included:** multi-region active-active deployment, autoscaling sophistication, full SOC-style compliance tooling, or speculative microservices.

**Exit criteria:** deployments are reproducible, rollbackable, monitored, and do not require production secrets in source control.

## Roadmap control and interface discipline

| Milestone | Status at 2026-07-18 | Entry evidence | Exit evidence |
| --- | --- | --- | --- |
| M0 | Not started | repository baseline recorded | runnable local vertical slice and smoke report |
| M1 | Blocked on M0 | M0 contracts and sample data path | validation report and CI gate |
| M2 | Blocked on M1 | valid curated corpus and schemas | repeatable index and relevance report |
| M3 | Blocked on M2 | source-preserving retrieval contract | grounded/tool policy evaluation report |
| M4 | Blocked on M3 | stable API and versioned SSE contract | accessible, responsive demo journey |
| M5 | Blocked on M0–M4 | all prior exit evidence | clean deploy/rollback rehearsal and monitoring |

Before a boundary change, write or update the smallest typed contract that defines it. This includes request/response Pydantic models, SSE event schemas, JSON schemas, Qdrant payload mapping, tool input/output models, and TypeScript client types. An incompatible public change needs a version, compatibility adapter, or migration decision. Stable dataset IDs, citation IDs, collection aliases, and event names must not change incidentally.

### Testing strategy and quality gates

| Layer | Required evidence | Examples |
| --- | --- | --- |
| Unit | Deterministic fast tests for pure policy/transform code. | validators, IDs, distance, cache keys, intent parser, citation mapper |
| Integration | Contract tests at service boundaries with external dependencies faked or disposable. | FastAPI routes, session ownership, SSE sequence, Qdrant/Redis adapters |
| Regression/evaluation | Fixed fixtures for a previously broken or demo-critical scenario. | food constraints, metro route, prompt injection, empty retrieval, stale weather |
| Negative/resilience | Safe handling of invalid/missing/unauthorized/dependency-failure inputs. | bad coordinates, denied location, tool timeout, malformed payload, cancellation |
| Release smoke | Short end-to-end checks against the released topology. | health, migrate, index sample, cited streamed answer, frontend route |

Every change runs the targeted row(s) above plus the closest available project-wide check. Mock at provider adapters, never with production credentials. Test failures are classified as code, flaky test, fixture/data, unavailable dependency, ambiguous requirement, or environment; after two materially different failed attempts, capture evidence and escalate rather than bypassing the guard.

### Observability requirements

At every API request, emit a correlation/request ID, route, status class, duration, release/version, and safe dependency classification. Never log credentials, tokens, raw private location, full prompt text, or unredacted PII. Instrument and dashboard p50/p95 for API, embedding, retrieval, reranking, tool, LLM first-token/completion, cache hit rate, SSE error/reconnect rate, validation duration, dataset freshness, citation rate, and grounded-answer evaluation pass rate. Tracing hooks must propagate the request ID through safe internal calls. Alerts should start with dependency unavailability, elevated error rate, and sustained latency/freshness breach; avoid noisy alerts for one-off demo-provider errors.

### Documentation requirements

Update only the documents that the change actually affects, but do not omit a durable contract. This includes README setup and commands, API/SSE schemas, architecture/data-flow documentation, environment-variable reference, dataset/source policy, migration/index notes, rollout/rollback runbook, and troubleshooting guide. Documentation must distinguish **implemented**, **planned**, and **deprecated** behavior, and its commands must be verified against the repository.

## Risk register

| Risk | Impact | Likelihood | Mitigation and trigger |
| --- | --- | --- | --- |
| Inaccurate or stale local data | High | Medium | Require source/freshness fields, validation, citations, and abstention; revalidate before demo. |
| External API or OSRM downtime | High | Medium | Typed adapters, <=3s timeout, cache where allowed, feature flag, and transparent fallback. |
| Embedding model/schema change | High | Medium | Versioned collection, content hashes, fixed evaluations, alias rollback; never mix vectors. |
| Qdrant corruption or bad re-index | High | Low | Versioned collections, disposable smoke build, alias cutover, retained prior collection. |
| Firebase/auth misconfiguration | High | Medium | Server-side verification, anonymous-policy tests, documented environment checks, deny-by-default protected paths. |
| Missing/misconfigured environment variable | Medium | High | Typed startup validation, `.env.example`, readiness diagnostics without secret values, CI config test. |
| Provider rate limits or cost spike | Medium | Medium | Request bounds, cache/TTL, concurrency cap, budgeted context, safe retry-after handling. |
| Location privacy leak | High | Low | Opt-in collection, rounding/minimal retention, redacted logs, no long-term precise-location analytics. |
| SSE instability on mobile networks | Medium | Medium | Event IDs/versioning, reconnect UI, cancellation tests, partial-answer state. |
| Hackathon scope creep | High | High | Demo-priority order, explicit non-goals, finish one vertical slice before secondary features. |

## Deployment, rollout, and rollback

Use this sequence for a state-changing release. Each arrow is a checked gate, not a cue to run work in parallel without evidence.

```text
Backup / release record
  → reviewed database migration
  → dataset validation
  → versioned index rebuild and evaluation
  → backend deployment + readiness
  → frontend deployment
  → release smoke tests
  → monitor metrics and demo-critical journeys
  → production traffic / demo handoff
```

Before rollout, record artifact versions, migration revision, dataset commit, collection alias/version, embedding model, prompt/tool version, environment change, health check, owner, and rollback decision. Roll back in reverse dependency order: stop/limit traffic if needed; revert frontend and backend artifacts; repoint the retrieval alias to the known-good collection; restore the known-good dataset commit; then use the reviewed migration downgrade or backup restore only when data compatibility requires it. Never run an untested destructive index deletion, migration downgrade, or broad data replacement in a shared environment.

## Lightweight decision records

Create a short record in `docs/decisions/` for a decision that changes a durable contract or is expensive to reverse: model/provider, collection versioning, auth policy, data schema, public API/SSE version, map/provider, retention, deployment topology, or feature flag policy. Each record contains: **date, owner, problem, decision, alternatives considered, consequences, rollout/rollback, and status**. Link the record from the affected milestone or README; do not create ADRs for routine implementation details.

## AI coding guidelines

1. Inspect the relevant code, schema, tests, and existing contract before editing; treat plans and provider output as untrusted context, not implementation truth.
2. Prefer existing abstractions and modify the smallest coherent surface. Do not rewrite working code, remove architectural comments, or refactor unrelated areas.
3. Respect the ownership table. Agree on an interface before parallel edits to a shared boundary, and keep commits logically grouped.
4. Keep public interfaces typed and schema-first. Do not use `any`, unchecked JSON, implicit defaults for safety behavior, or duplicate policy across backend and client.
5. Preserve source attribution, stable identifiers, WGS84 coordinates, freshness, error semantics, and backward compatibility through every transform.
6. Do not invent facts, quietly weaken validation/auth/rate limits, expose secrets, or turn tool/retrieved text into instructions.
7. Add or update the smallest meaningful test and documentation with every behavior/contract change. Report exact validation results and known limitations.

## Hackathon execution rules

Prioritize a reliable, user-visible vertical slice over breadth or polish. Use mature libraries; avoid speculative abstractions, microservices, and gold-plating. Finish and measure demo-critical chat, restaurant, weather, metro, map/nearby, and emergency journeys before secondary features. Optimize only after a measurement shows a budget breach. When tradeoffs are necessary, prefer citation integrity, safe failure, and deterministic demo behavior; record debt explicitly instead of disguising it as completeness.

## Work-item protocol

Every issue/PR must state the user outcome, scope, non-goals, required milestone/dependencies, owner/partners, API/data contract changes, source/index impact, security/privacy impact, risks, observability, verification commands, performance budget where applicable, rollout, and rollback. First inspect the relevant router, model, dataset, prompt, and tests. Make the smallest coherent change. Do not mix formatting-only churn with functional changes. Before handoff, run targeted tests plus the closest project-wide checks available, report exact commands/results, and identify known limitations.

Use this handoff template: **purpose; changed files; interface/schema changes; decisions/assumptions; tests and exact results; performance/validation evidence; risks; rollout/re-index/migration action; rollback; documentation changed; next owner.**

## Acceptance checklist

- Inputs are typed and bounded; failures return safe client messages and actionable server logs.
- Dataset-derived statements retain source identity and freshness.
- Lat/lon are WGS84 decimal degrees and validated before mapping, distance, or filtering.
- LLM answers do not fabricate opening hours, availability, fares, routes, emergency instructions, or citations.
- Live results supersede stale local values and disclose their timestamp/source where material.
- API changes are backward-compatible or explicitly versioned and documented.
- Tests cover happy path, invalid input, dependency timeout, unauthorized access, and regression behavior.
