# Submission process

Narrow scope: this repo does not host the proof-of-work itself — that lives in the
target module's own repo, per `hellfire-ai/.github`'s `CONTRIBUTING.md`. This repo
only tracks *applications for pool admission* built on top of that proof, and syncs
the resulting decision into `internal-db`.

## End-to-end flow

1. **Implement, in the open module repo.** Contractor follows `CONTRIBUTING.md`:
   opens an issue on the target module (e.g. `hellfire-ai/gtm-agent`) describing
   what they'll build, forks, implements against that module's README, opens a PR
   scoped to one module/one concern, gets it merged.
2. **Apply for verification, here.** Once the PR is merged, the contractor opens a
   [verification submission issue](../.github/ISSUE_TEMPLATE/verification-submission.yml)
   in `hellfire-ai/verification-layer` naming: GitHub username, target module code
   (must match a `crm.modules.code` / repo slug), optional vector/sub-area within
   that module, and the merged PR URL as evidence. One issue per module/vector —
   a contractor selling three modules submits three separate applications, each
   with its own evidence.
3. **Record the submission.** A reviewer (today: Bob; later: possibly delegated)
   converts the issue into a submission file under `submissions/<github_username>/<module_code>.yaml`
   via `verification-layer submit` (see [models.py](../src/verification_layer/models.py)).
   This file is the public, git-tracked record — visible in the same repo the
   philosophy points to ("public GitHub proof, not a résumé").
4. **Evaluate against the rubric.** Reviewer scores the evidence per
   [CRITERIA.md](CRITERIA.md) using `verification-layer score`, which writes the
   per-dimension scores and total into the submission file.
5. **Decide.** `verification-layer decide` sets `status` to `verified` or
   `rejected` based on the threshold in CRITERIA.md, stamps `decided_at`, and
   requires `notes` explaining the call (especially for rejections — the
   contractor should be able to read *why*, not just *that*).
6. **Sync to internal-db.** `verification-layer sync-db <path-to-submission.yaml>`
   upserts the decision into `crm.contractors` (see
   [INTERNAL_DB_SYNC.md](INTERNAL_DB_SYNC.md)). This is the only point where this
   repo talks to private infrastructure — the submission file itself never
   contains anything DSGVO-sensitive (just a GitHub username and a PR URL, both
   already public).
7. **Downstream consumers.** Once `nostr-tracker` (session 14) exists, it reads
   `verified` submission files to seed a contractor's first track-record event —
   see [NOSTR_HANDOFF.md](NOSTR_HANDOFF.md).

## Re-application

A `rejected` submission isn't permanent. The contractor can open a new PR
addressing the reviewer's notes and file a new submission issue referencing the
old one. Old submission files are never deleted or overwritten — a new decision
gets a new file revision in git history, so the audit trail (including past
rejections and why) stays intact.

## Scope boundary

This process verifies **relevance and authenticity of implementation work**, not
identity, tax status, or contractual terms — those remain Bob's/`internal-db`'s
concern. It also does not gate the issue/PR step on the module repos themselves;
`CONTRIBUTING.md` already covers that and this process does not duplicate it.
