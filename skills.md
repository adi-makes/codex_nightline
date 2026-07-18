# Ask Kochi Engineering Skills

> **Status (verified 2026-07-18):** Ask Kochi starts from project zero. This file
> specifies how to build the product; it does not claim that any application,
> dataset, integration, route, command, or infrastructure exists. `plan.md` is the
> ordered roadmap and `agents.md` defines ownership and handoff rules.

## Product intent

Ask Kochi is a grounded local-city companion for Kochi, Kerala. It should help
residents and visitors discover places and understand transport, weather, routes,
events, and emergency information without presenting guesses as facts. A useful
answer is attributable, geographically sensible, clear about freshness, and safe
when evidence or a live dependency is unavailable.

The proposed product is not a general-purpose chatbot, booking platform, emergency
authority, medical or legal adviser, or unrestricted web scraper. It must not invent
opening hours, prices, availability, routes, weather, events, safety instructions, or
citations.

## Working from a zero-state repository

Before adding implementation, inspect the repository and record what is actually
present. The only verified project artifacts at this baseline are planning and
guidance documents, an empty README, a license, and an image. Do not refer to
proposed paths, providers, environment variables, API events, commands, data fields,
or performance results as if they already exist.

Create only the smallest vertical slice needed for the approved milestone. Each
slice begins with a compact brief containing:

- user outcome and observable acceptance criteria;
- in-scope paths, owner, integrator, and required reviewers;
- proposed API, schema, tool, or UI contract and compatibility expectations;
- source/provenance and freshness requirements, if data is involved;
- security and privacy posture, failure behavior, rollout/rollback, and verification.

Stop for a decision when an unknown changes a public contract, data authority,
authentication/authorization boundary, provider selection, retention policy, or a
destructive migration or re-index. Otherwise make the smallest safe assumption and
label it **proposed**.

## Shared engineering rules

- Inspect existing code, schema, tests, configuration, and call sites before editing.
- Treat curated JSON as the factual source of truth; derived documents, vector
  payloads, caches, and model prose are not canonical data.
- Define and validate typed boundaries before crossing a service, data, tool, or UI
  boundary. Preserve stable IDs and source identity through every transform.
- Prefer small composable modules, deterministic transforms, explicit settings,
  bounded retries/timeouts, and reversible configuration over speculative framework
  layers or custom infrastructure.
- Keep user-visible failures honest. A bounded fallback or abstention is preferable
  to fabricated certainty or stale live data represented as current.
- Do not put credentials, tokens, private prompts, raw PII, or precise private
  locations in source, tests, logs, vector payloads, or browser code.
- Never weaken validation, authentication, authorization, CORS, rate limits,
  migrations, or tests merely to make a demo work.
- Document a durable change to an API/SSE contract, schema, source policy, prompt,
  environment variable, migration, index version, or runbook in the relevant docs.

## Proposed architecture boundaries

The planned architecture is a React/TypeScript PWA communicating with a FastAPI
service. The service is the proposed trust boundary for validation, authorization,
tool execution, retrieval, LLM calls, citations, and persistence. PostgreSQL,
Redis, Qdrant, and external live tools are proposed dependencies—not selected or
configured services at this baseline.

When a feature establishes one of these components, keep the following boundaries:

| Concern | Proposed source of truth / rule |
| --- | --- |
| Curated local facts | Version-controlled JSON with source and freshness metadata |
| Data shapes | Version-controlled JSON Schema and typed API/tool models |
| Database structure | Append-only reviewed migrations |
| Retrieval | Versioned, derived index payloads linked to stable source IDs |
| LLM policy | Version-controlled prompts and structured orchestration rules |
| Browser | Presentation and user interaction only; never secrets or server policy |
| Live data | Typed server-side adapters with source, timestamp, timeout, and safe fallback |

## Backend skill

If and when the backend is created, target Python 3.12+, FastAPI, Pydantic v2, and
async I/O. Keep routes thin; place business logic in focused services and inject
request-scoped dependencies. Validate and bound every external input, use explicit
timeouts and cancellation, map errors safely, and avoid synchronous network or
CPU-heavy work in async routes.

Define a public request/response or SSE schema before implementing it. Use deliberate
status codes, request IDs, safe structured logs, and tests for valid, invalid,
unauthorized, cancelled, and dependency-failure paths. Do not invent health,
session, or chat route names until the M0 contract records them.

## Frontend skill

If and when the frontend is created, use React functional components, TypeScript
strict mode, typed/validated API data, semantic HTML, and accessible error/loading
states. No `any`. Every interactive control needs an accessible name, keyboard path,
visible focus, and a usable small-screen layout.

Location is opt-in and must have a manual/named-location fallback. Validate WGS84
coordinates before display or calculation. Label straight-line distance separately
from a route distance, and never imply that time-sensitive content is fresh while
offline.

## Data, retrieval, and AI skill

Every curated record must be traceable to an appropriate source. Define schemas
before records, preserve stable IDs, normalize categories deliberately, validate
coordinates and URLs where present, and record freshness/estimation explicitly. Do
not manufacture demo data that is presented as verified local fact.

Build indexing as a deterministic, idempotent transform from validated source data.
Derived documents and chunks must retain parent ID, source reference, content hash,
schema/index version, and citation-ready metadata. Never manually patch the vector
store to fix a data issue, mix incompatible embedding models in a collection, or
re-index blindly after a model change.

Retrieve evidence before generation. Bound retrieval candidates, reranking, context,
tool concurrency, retries, and output tokens. Prompts, user messages, retrieved text,
and tool output are untrusted input: none can alter system policy. Model answers must
cite provided evidence, distinguish verified facts from estimates, and abstain or ask
one focused question when decisive evidence is absent.

## Geo, live-tool, and privacy skill

Use WGS84 decimal degrees, never swap latitude and longitude, and validate ranges at
the boundary. Nearby search should use a bounded candidate filter followed by an
exact great-circle calculation; routing must use a routing result rather than
presenting straight-line distance as travel distance. Minimize retention of user
location and redact it from logs.

Live adapters require typed input/output models, source/timestamp handling, a clear
freshness policy, an explicit timeout, and safe behavior when unavailable. Only retry
safe idempotent reads. Do not expose provider errors, credentials, or unsupported
claims to the user.

## Verification and handoff skill

Add focused tests with behavior changes: happy path, invalid/boundary inputs, and
the relevant failure path. Isolate external services behind adapters or disposable
test dependencies. Run the closest available formatter, linter, type checker,
validator, and targeted tests; when a command has not been created yet, state that
fact rather than claiming it was run.

Review the final diff for accidental scope expansion, secret/PII exposure, contract
compatibility, source attribution, accessibility, and rollback implications. A
handoff reports exact files, interfaces, verified/proposed decisions, commands and
observed results, migration/re-index actions, rollback, documentation, risks, and
the next owner. See `agents.md` for the required handoff format.

## Documentation and debt

Documentation must distinguish **implemented**, **planned**, and **deprecated**
behavior. Verify commands against the repository before publishing them. Record a
temporary compromise as `TODO(owner): rationale — removal condition`; never use a
TODO to conceal a security, correctness, provenance, or authorization gap.
