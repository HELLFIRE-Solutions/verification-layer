from datetime import datetime, timezone
from pathlib import Path

from verification_layer.models import Submission
from verification_layer.store import iter_submissions, load_submission, save_submission


def test_save_and_load_roundtrip(tmp_path: Path):
    submission = Submission(
        github_username="alice",
        module_code="gtm-agent",
        evidence_url="https://github.com/HELLFIRE-Solutions/gtm-agent/pull/12",
        relevance_note="Implemented lead qualification scoring.",
        submitted_at=datetime.now(timezone.utc),
    )
    path = save_submission(submission, root=tmp_path)
    assert path == tmp_path / "alice" / "gtm-agent.yaml"

    loaded = load_submission(path)
    assert loaded.github_username == "alice"
    assert loaded.module_code == "gtm-agent"


def test_iter_submissions_finds_all(tmp_path: Path):
    for username, module in [("alice", "gtm-agent"), ("bob", "office-agent")]:
        save_submission(
            Submission(
                github_username=username,
                module_code=module,
                evidence_url=f"https://github.com/HELLFIRE-Solutions/{module}/pull/1",
                relevance_note="note",
                submitted_at=datetime.now(timezone.utc),
            ),
            root=tmp_path,
        )
    found = iter_submissions(root=tmp_path)
    assert len(found) == 2


def test_iter_submissions_empty_dir(tmp_path: Path):
    assert iter_submissions(root=tmp_path / "does-not-exist") == []
