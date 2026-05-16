import unittest

from backend.analyzer.framework import (
    build_default_assignment_rules,
    build_default_call_rules,
)
from backend.analyzer.types import ResolutionReason, ResolutionStatus


class ResolutionFrameworkTests(unittest.TestCase):
    def test_resolution_status_and_reason_constants_are_centralized(self) -> None:
        self.assertEqual(ResolutionStatus.RESOLVED, "resolved")
        self.assertEqual(ResolutionStatus.AMBIGUOUS, "ambiguous")
        self.assertEqual(ResolutionReason.CONSTRUCTOR_CALL, "constructor_call")
        self.assertEqual(ResolutionReason.INSTANCE_METHOD, "instance_method")

    def test_default_call_rules_are_registered_in_explicit_order(self) -> None:
        rule_names = [rule.name for rule in build_default_call_rules()]
        self.assertEqual(
            rule_names,
            [
                "local-function",
                "constructor-call",
                "imported-function",
                "ambiguous-import",
                "top-level",
                "self-method",
                "instance-method",
                "module-alias-function",
                "module-function",
                "class-method",
            ],
        )

    def test_default_assignment_rules_are_registered_in_explicit_order(self) -> None:
        rule_names = [rule.name for rule in build_default_assignment_rules()]
        self.assertEqual(
            rule_names,
            [
                "constructor-assignment",
                "factory-assignment",
            ],
        )


if __name__ == "__main__":
    unittest.main()
