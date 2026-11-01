"""Deterministic mission contract with fail-closed human approval gates."""

from dataclasses import dataclass, field
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
    """Raised when a mission requiring approval lacks explicit human approval."""


@dataclass(frozen=True)
class Mission:
    """Immutable mission input; lifecycle state is only changed by transition()."""

    mission_id: str
    objective: str
    requested_actions: tuple[str, ...] = ()
    status: MissionStatus = field(default=MissionStatus.PROPOSED, init=False)
    human_approved: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.mission_id, str) or not self.mission_id.strip():
            raise ValueError("mission_id must be a non-empty string")
        if not isinstance(self.objective, str) or not self.objective.strip():
            raise ValueError("objective must be a non-empty string")
        actions = self.requested_actions
        if not isinstance(actions, (tuple, list)):
            raise TypeError("requested_actions must be a tuple or list of strings")
        if any(not isinstance(action, str) or not action.strip() for action in actions):
            raise ValueError("requested_actions must contain non-empty strings")
        object.__setattr__(self, "requested_actions", tuple(actions))

    @property
    def approval_required(self) -> bool:
        # No action is implicitly trusted. Unknown and newly introduced actions
        # therefore require the same explicit approval as classified sensitive actions.
        return bool(self.requested_actions)


def transition(
    mission: Mission,
    target: MissionStatus,
    *,
    human_approved: bool = False,
) -> Mission:
    """Return a new lifecycle state; this function never executes requested actions."""
    if not isinstance(mission, Mission):
        raise TypeError("mission must be a Mission")
    if not isinstance(target, MissionStatus):
        raise TypeError("target must be a MissionStatus")
    if not isinstance(human_approved, bool):
        raise TypeError("human_approved must be a bool")

    allowed = {
        MissionStatus.PROPOSED: {
            MissionStatus.APPROVED,
            MissionStatus.REJECTED,
            MissionStatus.BLOCKED,
            MissionStatus.CANCELLED,
        },
        MissionStatus.APPROVED: {
            MissionStatus.RUNNING,
            MissionStatus.CANCELLED,
            MissionStatus.BLOCKED,
        },
        MissionStatus.RUNNING: {
            MissionStatus.VERIFIED,
            MissionStatus.BLOCKED,
            MissionStatus.CANCELLED,
        },
        MissionStatus.VERIFIED: {
            MissionStatus.ACCEPTED,
            MissionStatus.REJECTED,
            MissionStatus.BLOCKED,
        },
    }
    if target not in allowed.get(mission.status, set()):
        raise ValueError(
            f"invalid mission transition: {mission.status.value} -> {target.value}"
        )
    if target == MissionStatus.APPROVED and mission.approval_required and not human_approved:
        raise ApprovalRequired(
            "explicit human approval is required for missions with requested actions"
        )

    # dataclasses.replace() cannot update init=False fields. Construct a fresh
    # frozen instance internally so callers cannot inject lifecycle state.
    updated = object.__new__(Mission)
    object.__setattr__(updated, "mission_id", mission.mission_id)
    object.__setattr__(updated, "objective", mission.objective)
    object.__setattr__(updated, "requested_actions", mission.requested_actions)
    object.__setattr__(updated, "status", target)
    object.__setattr__(
        updated,
        "human_approved",
        mission.human_approved or (target == MissionStatus.APPROVED and human_approved),
    )
    return updated
