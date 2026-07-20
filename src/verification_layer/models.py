from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from .criteria import MIN_DIMENSION_SCORE, VERIFIED_THRESHOLD, is_known_module


class SubmissionStatus(str, Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"


class CriteriaScore(BaseModel):
    relevance: int = Field(ge=0, le=3)
    functionality: int = Field(ge=0, le=3)
    scope_discipline: int = Field(ge=0, le=3)
    originality: int = Field(ge=0, le=3)

    @property
    def total(self) -> int:
        return self.relevance + self.functionality + self.scope_discipline + self.originality

    @property
    def dimensions(self) -> list[int]:
        return [self.relevance, self.functionality, self.scope_discipline, self.originality]

    def passes(self) -> bool:
        return self.total >= VERIFIED_THRESHOLD and all(d >= MIN_DIMENSION_SCORE for d in self.dimensions)


class Submission(BaseModel):
    github_username: str
    module_code: str
    vector: str | None = None
    evidence_url: str
    relevance_note: str
    submitted_at: datetime
    status: SubmissionStatus = SubmissionStatus.pending
    score: CriteriaScore | None = None
    evaluated_by: str | None = None
    notes: str | None = None
    decided_at: datetime | None = None

    @field_validator("module_code")
    @classmethod
    def module_should_be_known(cls, v: str) -> str:
        if not is_known_module(v):
            raise ValueError(
                f"unknown module_code {v!r} — check crm.modules / criteria.MODULE_RELEVANCE, "
                "or confirm this is a deliberately new module before proceeding"
            )
        return v

    @field_validator("evidence_url")
    @classmethod
    def evidence_should_be_a_pr(cls, v: str) -> str:
        if "/pull/" not in v:
            raise ValueError(f"evidence_url {v!r} doesn't look like a PR URL (expected '.../pull/<n>')")
        return v

    def decide(self, score: CriteriaScore, evaluated_by: str, notes: str) -> None:
        self.score = score
        self.evaluated_by = evaluated_by
        self.notes = notes
        self.status = SubmissionStatus.verified if score.passes() else SubmissionStatus.rejected
        self.decided_at = datetime.now(timezone.utc)
