# Evaluation criteria

The question this rubric answers: **does the submitted evidence (a merged PR) show
a relevant, working, honestly-scoped implementation of the specific module/vector
the contractor wants to sell** — as opposed to a generic side project, a tutorial
copy, or an unrelated contribution padded into the application.

This is deliberately not a general code-quality review. A rough-edged but genuinely
relevant implementation should outscore a polished but generic one.

## Scoring

Four dimensions, each scored 0–3 by the reviewer:

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Relevance** | Unrelated to the claimed module/vector | Tangentially related (same broad domain, wrong vector) | Implements the claimed vector but misses key parts of the module's README scope | Squarely implements the claimed module/vector |
| **Functionality** | Doesn't run / no evidence it was ever run | Runs but core claimed behavior is stubbed or broken | Runs and does what it claims for the happy path | Runs, handles the stated edge cases, has some form of test coverage |
| **Scope discipline** | Sprawling PR touching unrelated areas, or trivial (few-line) change | Scoped but noticeably larger than the concern warrants | One module, one concern, reviewable in a normal PR review pass | Same, plus a clear issue-then-PR trail per `CONTRIBUTING.md` |
| **Originality** | Copy-pasted tutorial/boilerplate with cosmetic renames | Heavily templated with limited original logic | Mostly original, some scaffolding from a known template | Original design decisions visible in the diff (naming, structure, tradeoffs explained in PR description) |

**Total: 0–12.** Threshold for `verified`: **total ≥ 9 AND no dimension scored 0.**
A 0 in any single dimension is disqualifying regardless of total — e.g. a 3/3/3/0
(unoriginal boilerplate, however functional) does not pass.

Scores 6–8 with no 0s: reviewer discretion — default to `rejected` with notes on
what would flip it, since re-application is cheap (see [PROCESS.md](PROCESS.md#re-application)).

Every decision — verified or rejected — requires `notes` on the submission record
explaining the score. This is what makes the process auditable instead of arbitrary.

## What "relevant" means per module

Mirrors `crm.modules` in `internal-db` (session 04) — descriptions kept in sync
manually; source of truth for the module list itself is `internal-db`'s
`migrations/0006_seed_modules.sql`. See [criteria.py](../src/verification_layer/criteria.py)
for the machine-readable form.

- **gtm-agent** (AI GTM / AI Sales) — warm-lead qualification logic, personalized
  outreach generation, demo-booking flow, or a CRM integration (e.g. HubSpot) that
  moves leads through a pipeline. *Not relevant:* a generic cold-email sender with
  no qualification/scoring step.
- **office-agent** (AI Office) — email triage/classification, internal knowledge
  base search (retrieval over internal docs), or document automation. *Not
  relevant:* a plain calendar or todo app with no retrieval/triage component.
- **rag-01** (RAG infra) — retrieval-augmented generation infrastructure: chunking,
  embedding, indexing, retrieval-then-generate pipeline. *Not relevant:* calling an
  LLM API with no retrieval step.
- **uni-tag** (UNI Tag / GEO-AEO) — `llms.txt` generation, schema.org markup,
  agent-readable meta tags, or measurable AI-search-visibility tooling. *Not
  relevant:* generic SEO scripts with no AI-agent-readability angle.
- **mcp-dev** (AI MCP Dev) — an MCP server implementation against a real or
  plausible client CRM/API surface. *Not relevant:* an MCP "hello world" with no
  real tool/resource logic.
- **inhouse-llm** (In-house LLM) — self-hosting/serving an open-source model
  (inference server, fine-tuning pipeline, quantization/deployment work). *Not
  relevant:* a wrapper around a hosted third-party API.
- **compliance-layer** (Compliance/Trust layer) — DSGVO/AI Act compliance tooling,
  audit-trail logic, or something built recognizably on TWIRA's trust-weighting
  principle. *Not relevant:* a generic form-validation library.
- **onboarding** (Onboarding/Training) — structured onboarding material generation
  or tooling (docs, guided walkthroughs, video/guide scaffolding tied to one of the
  other modules). *Not relevant:* a generic static-site-generator template with no
  onboarding-specific content.
- **verification-layer / nostr-tracker** (cross-cutting infra) — not client-sellable
  modules (deliberately excluded from `crm.modules`), but a PR against either of
  these two repos themselves is valid evidence if the contractor is applying to
  work on the infra itself rather than a client module.

If a contractor's evidence targets a vector not listed above, the reviewer judges
relevance against that module's own README rather than this list — this table is a
reviewer aid, not an exhaustive spec.

## Same rubric, human or AI

This rubric is intentionally not phrased in terms of "the person" — it scores the
artifact (the PR) against the claimed vector. That's the same trust-weighting shape
TWIRA (TETA+PI) applies when routing intent to AI agents: verify the demonstrated
capability against the claimed capability, not the credential. Applying it to
contractor onboarding here is the human-facing instance of that same principle.
