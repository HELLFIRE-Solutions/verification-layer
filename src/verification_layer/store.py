"""Submission records as one YAML file per (github_username, module_code) pair.

Deliberately not a database: these files ARE the public audit trail the
verification philosophy points to (see docs/PROCESS.md) — a contractor's
verification history should be readable in the same repo/git history a
reviewer used to decide it, not locked in a private table.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from .models import Submission

DEFAULT_SUBMISSIONS_DIR = Path("submissions")


def submission_path(github_username: str, module_code: str, root: Path = DEFAULT_SUBMISSIONS_DIR) -> Path:
    return root / github_username / f"{module_code}.yaml"


def save_submission(submission: Submission, root: Path = DEFAULT_SUBMISSIONS_DIR) -> Path:
    path = submission_path(submission.github_username, submission.module_code, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.loads(submission.model_dump_json(exclude_none=True))
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
    return path


def load_submission(path: Path) -> Submission:
    payload = yaml.safe_load(path.read_text())
    return Submission.model_validate(payload)


def iter_submissions(root: Path = DEFAULT_SUBMISSIONS_DIR) -> list[Submission]:
    if not root.exists():
        return []
    return [load_submission(p) for p in sorted(root.glob("*/*.yaml"))]
