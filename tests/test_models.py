from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from verification_layer.models import CriteriaScore, Submission


def make_submission(**overrides):
    defaults = dict(
        github_username="alice",
        module_code="gtm-agent",
        evidence_url="https://github.com/HELLFIRE-Solutions/gtm-agent/pull/12",
        relevance_note="Implemented lead qualification scoring.",
        submitted_at=datetime.now(timezone.utc),
    )
    defaults.update(overrides)
    return Submission(**defaults)


def test_rejects_unknown_module():
    with pytest.raises(ValidationError):
        make_submission(module_code="not-a-real-module")


def test_rejects_non_pr_evidence():
    with pytest.raises(ValidationError):
        make_submission(evidence_url="https://github.com/HELLFIRE-Solutions/gtm-agent")


def test_decide_verified_above_threshold():
    submission = make_submission()
    score = CriteriaScore(relevance=3, functionality=3, scope_discipline=3, originality=2)
    submission.decide(score=score, evaluated_by="bob", notes="Solid, relevant HubSpot integration.")
    assert submission.status.value == "verified"
    assert submission.decided_at is not None


def test_decide_rejected_on_zero_dimension():
    submission = make_submission()
    score = CriteriaScore(relevance=3, functionality=3, scope_discipline=3, originality=0)
    submission.decide(score=score, evaluated_by="bob", notes="Boilerplate copy, no original logic.")
    assert submission.status.value == "rejected"


def test_decide_rejected_below_threshold():
    submission = make_submission()
    score = CriteriaScore(relevance=2, functionality=2, scope_discipline=2, originality=1)
    submission.decide(score=score, evaluated_by="bob", notes="Partially relevant, needs more depth.")
    assert submission.status.value == "rejected"
