from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FreeLLMAPIAdoptionTests(unittest.TestCase):
    def test_required_adoption_artifacts_exist(self):
        required = [
            "governance/decisions/ADR-0005-freellmapi-universal-inference-fabric.md",
            "governance/inference-policy.yaml",
            "missions/KIA-2026-005.yaml",
            "scripts/preflight_freellmapi.sh",
            "scripts/verify_freellmapi.py",
        ]
        for item in required:
            self.assertTrue((ROOT / item).is_file(), item)

    def test_inference_policy_is_fail_closed(self):
        policy = (ROOT / "governance/inference-policy.yaml").read_text(encoding="utf-8")
        self.assertIn("default_decision: block", policy)
        self.assertIn("PAID_INFRA", policy)
        self.assertIn("UNKNOWN", policy)
        self.assertIn("public_exposure: blocked", policy)

    def test_mission_does_not_claim_completion(self):
        mission = (ROOT / "missions/KIA-2026-005.yaml").read_text(encoding="utf-8")
        self.assertIn("status: approved", mission)
        self.assertIn("fallback contrôlé", mission)
        self.assertNotIn("status: closed", mission)

    def test_verifier_writes_only_ignored_private_evidence(self):
        verifier = (ROOT / "scripts/verify_freellmapi.py").read_text(encoding="utf-8")
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn('"artifacts" / "private"', verifier)
        self.assertIn("artifacts/private/", gitignore)

    def test_live_inference_requires_explicit_shell_unlock(self):
        verifier = (ROOT / "scripts/verify_freellmapi.py").read_text(encoding="utf-8")
        self.assertIn("KIANGANA_ALLOW_LIVE_INFERENCE", verifier)
        self.assertIn('!= "YES"', verifier)


if __name__ == "__main__":
    unittest.main()
