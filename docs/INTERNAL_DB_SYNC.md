# internal-db sync

## What this repo writes

`verification-layer sync-db <submission.yaml>` connects to `internal-db`
(session 04, private repo) via `DATABASE_URL` and runs a single `UPDATE` against
the existing `crm.contractors` table:

```sql
UPDATE crm.contractors
SET verification_status = <submission.status>,   -- 'verified' | 'rejected'
    verified_at = <submission.decided_at>         -- only set when status = 'verified'
WHERE github_username = <submission.github_username>
```

See [db_sync.py](../src/verification_layer/db_sync.py). No new tables, no schema
changes — this repo consumes `crm.contractors` as it already exists (columns
`github_username`, `verification_status`, `verified_at` were already present in
`internal-db/migrations/0003_contractors.sql`, session 04's own design).

## Why UPDATE-only, no INSERT

`crm.contractors.full_name` is `NOT NULL`. This repo only ever has a GitHub
username and a PR URL — it has no legitimate source for a contractor's real name,
email, or contract terms. Fabricating a placeholder would plant bad data in a
DSGVO-sensitive table. So: **the contractor row must already exist** (created
through internal-db's own onboarding process, whatever that turns out to be —
Bob manually, or a future intake form) before `sync-db` can attach a verification
decision to it. If no row matches, `sync-db` fails loudly with the
`github_username` it couldn't find, rather than guessing.

Practical implication for the process in [PROCESS.md](PROCESS.md): a contractor
should have at least a bare contractor record (name + github_username) in
`internal-db` *before* their verification submission is decided, or `sync-db`
will need a re-run once that record exists.

## What's NOT synced

The per-submission detail — module/vector claimed, evidence URL, rubric scores,
reviewer notes — stays in this repo's `submissions/*.yaml` files, not in
`internal-db`. `crm.contractors.verification_status` is a single coarse enum
(`unverified/pending/verified/rejected`) with no room for "verified for which
module." A contractor selling three modules with one verified and two rejected
submissions would collapse to a single `verified` status in `internal-db` today.

This is a known gap, not an oversight — extending the schema is session 04's
call, not this repo's to make unilaterally. If per-module granularity in
`internal-db` becomes necessary (e.g. once contracts are scoped per-module and a
client needs to know a contractor is verified specifically for `mcp-dev`, not
just "verified" in general), the natural fix is a `crm.contractor_verifications`
join table (`contractor_id`, `module_id`, `status`, `evidence_url`,
`decided_at`) — flagged here for whoever picks up session 04 next, not applied
by this session.

## Local testing

Not exercised against a live Postgres in this session — same constraint
`internal-db`'s own SCHEMA.md notes (no docker/psql available on this machine).
`sync_submission()` in `db_sync.py` was reviewed manually against
`internal-db/migrations/0003_contractors.sql`; real test is running it against
the session-02 server once both repos are deployed there.
