import unittest
from dataclasses import FrozenInstanceError

from jarvis.core import (
    ApprovalRequired,
    Mission,
    MissionStatus,
    SensitiveAction,
    transition,
)


class JarvisCoreApprovalHardeningTests(unittest.TestCase):
    def test_mission_requires_non_empty_identity_and_objective(self):
        with self.assertRaises(ValueError):
            Mission("", "Build a bounded core")
        with self.assertRaises(ValueError):
            Mission("JARVIS-001", "  ")
        with self.assertRaises(ValueError):
            Mission(None, "Objective")

    def test_lifecycle_fields_cannot_be_injected_at_construction(self):
        with self.assertRaises(TypeError):
            Mission("JARVIS-001", "Deploy", ("production_deployment",),
                    status=MissionStatus.APPROVED)
        with self.assertRaises(TypeError):
            Mission("JARVIS-001", "Deploy", ("production_deployment",),
                    human_approved=True)

    def test_mission_is_immutable(self):
        mission = Mission("JARVIS-001", "Document")
        with self.assertRaises(FrozenInstanceError):
            mission.status = MissionStatus.APPROVED

    def test_requested_actions_are_copied_to_an_immutable_tuple(self):
        actions = ["production_deployment"]
        mission = Mission("JARVIS-002", "Deploy", actions)
        actions.append("billing_change")
        self.assertEqual(mission.requested_actions, ("production_deployment",))

    def test_malformed_actions_fail_closed(self):
        with self.assertRaises(TypeError):
            Mission("JARVIS-003", "Deploy", "production_deployment")
        with self.assertRaises(ValueError):
            Mission("JARVIS-003", "Deploy", ("",))

    def test_sensitive_action_requires_explicit_approval(self):
        mission = Mission(
            "JARVIS-004",
            "Deploy",
            (SensitiveAction.PRODUCTION_DEPLOYMENT.value,),
        )
        with self.assertRaises(ApprovalRequired):
            transition(mission, MissionStatus.APPROVED)
        approved = transition(
            mission, MissionStatus.APPROVED, human_approved=True
        )
        self.assertEqual(approved.status, MissionStatus.APPROVED)
        self.assertTrue(approved.human_approved)

    def test_unknown_action_also_requires_approval(self):
        mission = Mission("JARVIS-005", "Run future action", ("unknown_capability",))
        self.assertTrue(mission.approval_required)
        with self.assertRaises(ApprovalRequired):
            transition(mission, MissionStatus.APPROVED)

    def test_no_action_mission_can_be_approved_without_sensitive_approval(self):
        mission = Mission("JARVIS-006", "Record a note")
        approved = transition(mission, MissionStatus.APPROVED)
        self.assertEqual(approved.status, MissionStatus.APPROVED)
        self.assertFalse(approved.human_approved)

    def test_approval_is_not_execution_and_original_is_unchanged(self):
        mission = Mission("JARVIS-007", "Send a message", ("external_communication",))
        approved = transition(mission, MissionStatus.APPROVED, human_approved=True)
        self.assertEqual(approved.status, MissionStatus.APPROVED)
        self.assertEqual(mission.status, MissionStatus.PROPOSED)
        self.assertFalse(mission.human_approved)

    def test_cannot_skip_approval_or_verification_stages(self):
        mission = Mission("JARVIS-008", "Deploy", ("production_deployment",))
        with self.assertRaises(ValueError):
            transition(mission, MissionStatus.RUNNING)
        approved = transition(mission, MissionStatus.APPROVED, human_approved=True)
        running = transition(approved, MissionStatus.RUNNING)
        verified = transition(running, MissionStatus.VERIFIED)
        self.assertEqual(verified.status, MissionStatus.VERIFIED)

    def test_verified_mission_requires_explicit_acceptance(self):
        mission = Mission("JARVIS-009", "Test")
        approved = transition(mission, MissionStatus.APPROVED)
        running = transition(approved, MissionStatus.RUNNING)
        verified = transition(running, MissionStatus.VERIFIED)
        self.assertEqual(
            transition(verified, MissionStatus.ACCEPTED).status,
            MissionStatus.ACCEPTED,
        )

    def test_invalid_transition_and_invalid_target_fail_closed(self):
        mission = Mission("JARVIS-010", "Test")
        with self.assertRaises(ValueError):
            transition(mission, MissionStatus.ACCEPTED)
        with self.assertRaises(TypeError):
            transition(mission, "approved")


if __name__ == "__main__":
    unittest.main()
