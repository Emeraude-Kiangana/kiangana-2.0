import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "student_system_baseline.py"
SPEC = importlib.util.spec_from_file_location("student_baseline", SCRIPT)
student_baseline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(student_baseline)


class StudentTechnologyBaselineTests(unittest.TestCase):
    def setUp(self):
        self.catalog = student_baseline.load_catalog()

    def test_catalog_is_dependency_free_machine_readable_yaml_subset(self):
        raw = (ROOT / "config" / "capabilities.yaml").read_text(encoding="utf-8")
        parsed = json.loads(raw)
        self.assertEqual(parsed["checkpoint"], "P05-CP-STUDENT-01")

    def test_every_capability_uses_an_allowed_zero_dollar_class(self):
        allowed = set(self.catalog["policy"]["allowed_classes"])
        self.assertEqual(
            allowed,
            {
                "ZERO_NATIVE",
                "ZERO_STUDENT",
                "ZERO_QUOTA",
                "CREDITED",
                "PAID_OPTIONAL",
            },
        )
        for item in self.catalog["capabilities"]:
            self.assertIn(item["class"], allowed)

    def test_zero_dollar_policy_blocks_automatic_paid_enablement(self):
        policy = self.catalog["policy"]
        self.assertEqual(policy["direct_spend_usd"], 0)
        self.assertFalse(policy["auto_enable_paid_services"])
        for item in self.catalog["capabilities"]:
            if item["class"] in {"CREDITED", "PAID_OPTIONAL"}:
                self.assertFalse(item["persistent_dependency_allowed"])

    def test_external_services_are_not_claimed_available(self):
        baseline = student_baseline.build_baseline(self.catalog)
        external = [
            item for item in baseline["capabilities"] if item["scope"] == "external"
        ]
        self.assertTrue(external)
        for item in external:
            self.assertEqual(item["status"], "UNKNOWN_EXTERNAL")
            self.assertIsNone(item["available"])

    def test_baseline_reports_zero_spend_and_zero_exposed_secrets(self):
        baseline = student_baseline.build_baseline(self.catalog)
        self.assertEqual(baseline["direct_spend_usd"], 0)
        self.assertEqual(baseline["secrets_exposed"], 0)
        self.assertFalse(baseline["paid_services_auto_enabled"])

    @patch.object(student_baseline, "_detect_wsl", return_value=(True, "test"))
    @patch.object(student_baseline, "_command_version", return_value=(True, "tool 1.0"))
    @patch.object(student_baseline.platform, "system", return_value="Linux")
    @patch.object(student_baseline.platform, "release", return_value="test")
    @patch.object(student_baseline.platform, "python_version", return_value="3.12.0")
    def test_required_local_capabilities_can_produce_ready_verdict(
        self,
        _python_version,
        _release,
        _system,
        _command_version,
        _detect_wsl,
    ):
        baseline = student_baseline.build_baseline(self.catalog)
        self.assertTrue(baseline["local_foundation_ready"])
        self.assertEqual(baseline["verdict"], "LOCAL_FOUNDATION_READY")

    def test_human_report_contains_no_account_identity_fields(self):
        baseline = student_baseline.build_baseline(self.catalog)
        report = student_baseline.render_human(baseline)
        for forbidden in ("username", "hostname", "home directory", "account id"):
            self.assertNotIn(forbidden, report.lower())


if __name__ == "__main__":
    unittest.main()
