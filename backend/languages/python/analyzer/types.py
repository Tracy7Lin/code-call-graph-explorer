from __future__ import annotations

from dataclasses import dataclass

from backend.core.semantics import SharedResolutionReason, SharedResolutionStatus


class ResolutionStatus(SharedResolutionStatus):
    pass


class ResolutionReason(SharedResolutionReason):
    pass


@dataclass(frozen=True)
class Resolution:
    callee_id: str
    resolved: bool
    confidence: str
    status: str
    reason: str
    candidate_symbol_ids: list[str]
