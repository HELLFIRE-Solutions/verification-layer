"""verification-layer CLI — see docs/PROCESS.md for the intended flow.

    verification-layer submit <github_username> <module_code> <evidence_url> "<relevance_note>" [--vector VECTOR]
    verification-layer decide <submission_yaml> --by <name> --relevance N --functionality N --scope-discipline N --originality N --notes "<notes>"
    verification-layer list
    verification-layer sync-db <submission_yaml>
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

from .db_sync import SyncError, sync_submission
from .models import CriteriaScore, Submission
from .store import iter_submissions, load_submission, save_submission


def cmd_submit(args: argparse.Namespace) -> None:
    try:
        submission = Submission(
            github_username=args.github_username,
            module_code=args.module_code,
            vector=args.vector,
            evidence_url=args.evidence_url,
            relevance_note=args.relevance_note,
            submitted_at=datetime.now(timezone.utc),
        )
    except ValidationError as exc:
        print(f"invalid submission: {exc}", file=sys.stderr)
        sys.exit(1)
    path = save_submission(submission)
    print(f"recorded submission: {path}")


def cmd_decide(args: argparse.Namespace) -> None:
    submission = load_submission(args.submission_yaml)
    score = CriteriaScore(
        relevance=args.relevance,
        functionality=args.functionality,
        scope_discipline=args.scope_discipline,
        originality=args.originality,
    )
    submission.decide(score=score, evaluated_by=args.by, notes=args.notes)
    path = save_submission(submission)
    print(f"{submission.github_username}/{submission.module_code}: {submission.status.value} (score {score.total}/12) -> {path}")


def cmd_list(args: argparse.Namespace) -> None:
    submissions = iter_submissions()
    if not submissions:
        print("no submissions on file")
        return
    for s in submissions:
        score_str = f"{s.score.total}/12" if s.score else "unscored"
        print(f"{s.github_username}/{s.module_code} ({s.vector or 'no vector'}): {s.status.value} [{score_str}]")


def cmd_sync_db(args: argparse.Namespace) -> None:
    submission = load_submission(args.submission_yaml)
    try:
        sync_submission(submission)
    except SyncError as exc:
        print(f"sync failed: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"synced {submission.github_username} -> crm.contractors.verification_status={submission.status.value}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="verification-layer")
    sub = parser.add_subparsers(dest="command", required=True)

    p_submit = sub.add_parser("submit", help="record a new verification submission")
    p_submit.add_argument("github_username")
    p_submit.add_argument("module_code")
    p_submit.add_argument("evidence_url")
    p_submit.add_argument("relevance_note")
    p_submit.add_argument("--vector", default=None)
    p_submit.set_defaults(func=cmd_submit)

    p_decide = sub.add_parser("decide", help="score a submission and decide verified/rejected")
    p_decide.add_argument("submission_yaml", type=Path)
    p_decide.add_argument("--by", required=True, help="reviewer name")
    p_decide.add_argument("--relevance", type=int, required=True)
    p_decide.add_argument("--functionality", type=int, required=True)
    p_decide.add_argument("--scope-discipline", type=int, required=True, dest="scope_discipline")
    p_decide.add_argument("--originality", type=int, required=True)
    p_decide.add_argument("--notes", required=True)
    p_decide.set_defaults(func=cmd_decide)

    p_list = sub.add_parser("list", help="list all submissions on file")
    p_list.set_defaults(func=cmd_list)

    p_sync = sub.add_parser("sync-db", help="push a decided submission's status into internal-db")
    p_sync.add_argument("submission_yaml", type=Path)
    p_sync.set_defaults(func=cmd_sync_db)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
