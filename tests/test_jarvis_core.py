import unittest

from jarvis.core import ApprovalRequired, Mission, MissionStatus, transition


class JarvisCoreContractTests(unittest.TestCase):
    def test_mission_requires_identity_and_objective(self):
        with self.assertRaises(ValueError):
            Mission("", "Build a bounded core")
        with self.assertRaises(ValueError):
            Mission("JARVIS-001", "  ")

    def test_non_sensitive_mission_can_be_approved(self):
        mission = Mission("JARVIS-001", "Document the core")
        approved = transition(mission, MissionStatus.APPROVED)
        self.assertEqual(approved.status, MissionStatus.APPROVED)
        self.assertFalse(approved.human_approved)

    def test_sensitive_action_requires_explicit_human_approval(self):
        mission = Mission("JARVIS-002", "Deploy", ("production_deployment",))
        with self.assertRaises(ApprovalRequired):
            transition(mission, MissionStatus.APPROVED)
        approved = transition(mission, MissionStatus.APPROVED, human_approved=True)
        self.assertTrue(approved.human_approved)

    def test_approval_is_not_execution(self):
        mission = Mission("JARVIS-003", "Send a message", ("external_communication",))
        approved = transition(mission, MissionStatus.APPROVED, human_approved=True)
        self.assertEqual(approved.status, MissionStatus.APPROVED)
        self.assertEqual(mission.status, MissionStatus.PROPOSED)

    def test_invalid_transition_is_rejected(self):
        mission = Mission("JARVIS-004", "Test")
        with self.assertRaises(ValueError):
            transition(mission, MissionStatus.ACCEPTED)

    def test_verified_mission_requires_explicit_acceptance(self):
        mission = Mission("JARVIS-005", "Test")
        approved = transition(mission, MissionStatus.APPROVED)
        running = transition(approved, MissionStatus.RUNNING)
        verified = transition(running, MissionStatus.VERIFIED)
        self.assertEqual(verified.status, MissionStatus.VERIFIED)
        self.assertEqual(transition(verified, MissionStatus.ACCEPTED).status, MissionStatus.ACCEPTED)


if __name__ == "__main__":
    unittest.main()
