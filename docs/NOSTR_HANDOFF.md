# Handoff to nostr-tracker (session 14)

`nostr-tracker` doesn't exist yet (session 14, not started). This document is
the data contract that session should consume — written now so verification-layer
doesn't need to change shape later to accommodate it.

## The idea

A contractor's Nostr track record is "independent, unforgeable, growing" (per
`nostr-tracker`'s own README) because each work-log entry is signed by their own
keypair, not written by HELLFIRE. But the *first* entry in that record has a
bootstrapping problem: nothing yet exists to sign. The natural first entry is the
verification event itself — proof that predates and justifies pool admission,
public before the contractor ever logged an hour.

## What verification-layer provides

A `verified` submission file under `submissions/<github_username>/<module_code>.yaml`
(schema: [models.py](../src/verification_layer/models.py)) contains everything
needed to construct that seed event:

| Field | Use in the Nostr event |
|---|---|
| `github_username` | Correlates to the contractor's `internal-db` record and, once assigned, their `nostr_pubkey` |
| `module_code` / `vector` | What capability is being attested |
| `evidence_url` | The actual proof — the merged PR — referenced or linked from the event content |
| `decided_at` | Event timestamp basis |
| `evaluated_by` | Attestation source (today: Bob; the human/process making the claim) |

## Expected flow once nostr-tracker exists

1. Contractor onboards to `nostr-tracker`, gets a keypair, `nostr_pubkey` gets
   set on their `internal-db` contractor row (session 04's existing nullable
   column, already designed for this).
2. `nostr-tracker` (or a one-off script within it) reads this repo's `verified`
   submission file(s) for that `github_username`.
3. It publishes one seed event per verified submission — content should include
   at minimum `module_code`, `evidence_url`, and `decided_at`, signed by the
   contractor's own key (an attestation *about* them, but published *by* them,
   consistent with the "belongs to the contractor, not the company" design goal
   stated in nostr-tracker's README).
4. Subsequent work-log events (per `internal-db`'s `work_log.nostr_event_id`)
   build on top of that first entry.

## Open questions (nostr-tracker's to resolve, not this repo's)

- Event kind: custom `kind` vs. an existing NIP that fits an "attestation"
  shape — session 14's own open question, listed in its README.
- Whether verification-layer or nostr-tracker owns publishing the seed event.
  This doc assumes nostr-tracker reads verification-layer's files and publishes,
  since nostr-tracker owns the relay/signing infrastructure and
  verification-layer has no reason to hold a contractor's key material.

## Same principle, human or AI (TWIRA)

Per the session-13 brief: this is the same trust-weighting shape TWIRA
(TETA+PI) applies to AI agents — a claimed capability gets checked against
demonstrated evidence before being trusted/routed to. Here the "claimed
capability" is a module/vector, the "evidence" is a merged PR, and the
"routing" is pool admission plus the first track-record entry. Full TWIRA
mechanics beyond this framing weren't in scope for this session — ask Bob
directly if `nostr-tracker` needs more than this doc provides.
