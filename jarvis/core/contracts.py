"""Minimal deterministic mission contract; no tools or external side effects."""

from dataclasses import dataclass, replace
from enum import Enum


class MissionStatus(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    RUNNING = "running"
    VERIFIED = "verified"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class SensitiveAction(str, Enum):
    FINANCIAL_TRANSACTION = "financial_transaction"
    PRODUCTION_DEPLOYMENT = "production_deployment"
    IRREVERSIBLE_DELETION = "irreversible_deletion"
    EXTERNAL_COMMUNICATION = "external_communication"
    BILLING_CHANGE = "billing_change"


class ApprovalRequired(PermissionError):
    """Raised when a sensitive action lacks explicit human approval."""


@dataclass(frozen=True)
class Mission:
    mission_id: str
    objective: str
    requested_actions: tuple[str, ...] = ()
    status: MissionStatus = MissionStatus.PROPOSED
    human_approved: bool = False

    def __post_init__(self) -> None:
        if not self.mission_id.strip():
            raise ValueError("mission_id must not be empty")
        if not self.objective.strip():
            raise ValueError("objective must not be empty")

    @property
    def approval_required(self) -> bool:
        sensitive = {action.value for action in SensitiveAction}
        return any(action in sensitive for action in self.requested_actions)


def transition(mission: Mission, target: MissionStatus, *, human_approved: bool = False) -> Mission:
    """Return a new mission state; never executes the requested actions."""
    allowed = {
        MissionStatus.PROPOSED: {MissionStatus.APPROVED, MissionStatus.REJECTED, MissionStatus.BLOCKED, MissionStatus.CANCELLED},
        MissionStatus.APPROVED: {MissionStatus.RUNNING, MissionStatus.CANCELLED, MissionStatus.BLOCKED},
        MissionStatus.RUNNING: {MissionStatus.VERIFIED, MissionStatus.BLOCKED, MissionStatus.CANCELLED},
        MissionStatus.VERIFIED: {MissionStatus.ACCEPTED, MissionStatus.REJECTED, MissionStatus.BLOCKED},
    }
    if target not in allowed.get(mission.status, set()):
        raise ValueError(f"invalid mission transition: {mission.status.value} -> {target.value}")
    if target == MissionStatus.APPROVED and mission.approval_required and not human_approved:
        raise ApprovalRequired("explicit human approval is required for sensitive actions")
    return replace(
        mission,
        status=target,
        human_approved=mission.human_approved or (target == MissionStatus.APPROVED and human_approved),
    )
