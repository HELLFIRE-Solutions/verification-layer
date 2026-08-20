# HELLFIRE AI Solutions — Verification Layer

Cross-cutting infrastructure (not a module). GitHub-based verification of contractors before pool admission: public GitHub proof of a relevant implementation of a module/vector — not a résumé, not a diploma. The basic process (issue → fork → scoped PR) is described in [`HELLFIRE-Solutions/.github`'s CONTRIBUTING.md](https://github.com/HELLFIRE-Solutions/.github/blob/main/CONTRIBUTING.md); this repo is what happens *after* the PR merges: pool-admission application, relevance scoring, status sync.

Related to `internal-db` (session 04, verification status) and the future Nostr Time-Tracker (session 14, a verified GitHub profile becomes the first track-record entry). The same verification principle (TWIRA — Trust-Weighted Intent Routing, from TETA+PI) applies to both people and AI agents — details in [`docs/CRITERIA.md`](docs/CRITERIA.md#same-rubric-human-or-ai).

## Documentation

- [`docs/PROCESS.md`](docs/PROCESS.md) — the end-to-end application process, 7 steps from a module issue to the internal-db sync.
- [`docs/CRITERIA.md`](docs/CRITERIA.md) — scoring rubric (4 dimensions, 0–3 each, verification threshold) + what counts as relevant for each of the 8 sellable modules.
- [`docs/INTERNAL_DB_SYNC.md`](docs/INTERNAL_DB_SYNC.md) — how and why the sync into `crm.contractors` is UPDATE-only, never INSERT (no legitimate source for `full_name`).
- [`docs/NOSTR_HANDOFF.md`](docs/NOSTR_HANDOFF.md) — data contract for session 14 (not started yet).
- [`.github/ISSUE_TEMPLATE/verification-submission.yml`](.github/ISSUE_TEMPLATE/verification-submission.yml) — the application form.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,db]"

verification-layer submit octocat gtm-agent \
  https://github.com/HELLFIRE-Solutions/gtm-agent/pull/12 \
  "Implemented HubSpot contact upsert matching architecture.md's integration point" \
  --vector hubspot-integration

verification-layer decide submissions/octocat/gtm-agent.yaml \
  --by bob --relevance 3 --functionality 3 --scope-discipline 3 --originality 2 \
  --notes "Squarely on-vector, ran it locally, scoped PR."

verification-layer list

cp .env.example .env  # DATABASE_URL, only needed for sync-db
verification-layer sync-db submissions/octocat/gtm-agent.yaml
```

`pytest tests/` — 8 tests (model + rubric validation, YAML store round-trip).

## Deliberate decisions

- **No automated scoring gate.** `decide` always requires a human reviewer (`--by`) and notes — locked in after session 11 (compliance-layer) flagged the risk of drifting into AI Act Annex III (high-risk) if this became an automated hiring gate with no human in the loop.
- **Files, not a DB, for application detail.** `submissions/*.yaml` is a public, git-tracked audit trail; `internal-db` only gets the coarse summary (verified/rejected), not the scoring detail.

**Status:** Tasks 1–4 from the kickoff prompt are done (process, criteria, internal-db sync, nostr-tracker handoff). Not tested against a live Postgres (same blocker as internal-db — no psql/docker on this machine).

**License:** MIT.
