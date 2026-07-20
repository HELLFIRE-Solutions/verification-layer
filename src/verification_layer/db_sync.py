"""Sync a decided submission into internal-db's crm.contractors.

Scope boundary: this only UPDATEs an existing contractor row matched by
github_username. It never INSERTs one, because crm.contractors.full_name is
NOT NULL and this repo has no legitimate source for that field — contractor
onboarding (name, email, contract) is internal-db's/Bob's process, not
something verification-layer should fabricate from a GitHub username. If no
matching row exists yet, sync fails loudly with instructions instead of
guessing.

Not exercised against a live Postgres in this session (no docker/psql
available here either — see internal-db/docs/SCHEMA.md's own note on this).
"""

from __future__ import annotations

import os

from .models import Submission, SubmissionStatus


class SyncError(Exception):
    pass


def sync_submission(submission: Submission, database_url: str | None = None) -> None:
    if submission.status == SubmissionStatus.pending:
        raise SyncError(f"submission for {submission.github_username}/{submission.module_code} is still pending — decide() first")

    database_url = database_url or os.environ.get("DATABASE_URL")
    if not database_url:
        raise SyncError("DATABASE_URL not set (see internal-db/.env.example)")

    import psycopg  # imported lazily: only needed for this one code path

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE crm.contractors
                SET verification_status = %s,
                    verified_at = CASE WHEN %s = 'verified' THEN %s ELSE verified_at END
                WHERE github_username = %s
                RETURNING id
                """,
                (
                    submission.status.value,
                    submission.status.value,
                    submission.decided_at,
                    submission.github_username,
                ),
            )
            row = cur.fetchone()
            if row is None:
                raise SyncError(
                    f"no crm.contractors row with github_username={submission.github_username!r} — "
                    "create the contractor record in internal-db first, then re-run sync-db"
                )
        conn.commit()
