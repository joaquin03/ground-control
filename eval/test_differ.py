import unittest
from differ import diff_case

CASE = {
    "id": "02-adriatic-departure", "decision": "HANDLE", "intent": "NEW", "op_status": "OPEN",
    "services": {"handling": "REQUESTED", "ground_transport": "REQUESTED", "catering": "REQUESTED", "hotel": "TBC"},
    "routing": {"ground_transport": "procurement", "hotel": "procurement"},
    "reason": None, "ref_expect": "assign",
}
GOOD = {
    "case": "02-adriatic-departure", "decision": "HANDLE", "intent": "NEW", "op_status": "OPEN",
    "confidence": "HIGH", "ref": "PN2606031",
    "services": {"handling": "REQUESTED", "ground_transport": "REQUESTED", "catering": "REQUESTED", "hotel": "TBC"},
    "routing": {"ground_transport": "procurement", "hotel": "procurement"}, "reason": [],
}

class TestDiff(unittest.TestCase):
    def test_all_pass(self):
        fails = diff_case(CASE, GOOD)
        self.assertEqual(fails, [])
    def test_wrong_decision_fails(self):
        bad = dict(GOOD, decision="ESCALATE")
        self.assertIn("decision", [f[0] for f in diff_case(CASE, bad)])
    def test_wrong_service_status_fails(self):
        bad = dict(GOOD, services=dict(GOOD["services"], hotel="REQUESTED"))
        self.assertIn("services", [f[0] for f in diff_case(CASE, bad)])
    def test_missing_routing_fails(self):
        bad = dict(GOOD, routing={"ground_transport": "procurement"})
        self.assertIn("routing", [f[0] for f in diff_case(CASE, bad)])
    def test_bad_ref_fails(self):
        bad = dict(GOOD, ref="NOPE")
        self.assertIn("ref", [f[0] for f in diff_case(CASE, bad)])

if __name__ == "__main__":
    unittest.main()
