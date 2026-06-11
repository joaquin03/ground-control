import unittest
from headers import parse_header

SAMPLE = """CASE: 02-adriatic-departure
DECISION: HANDLE   INTENT: NEW   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606031
SERVICES: handling=REQUESTED ground_transport=REQUESTED catering=REQUESTED hotel=TBC
ROUTING: ground_transport=procurement hotel=procurement
REASON: -
Some prose below that must be ignored.
"""

class TestParseHeader(unittest.TestCase):
    def test_scalar_fields(self):
        h = parse_header(SAMPLE)
        self.assertEqual(h["case"], "02-adriatic-departure")
        self.assertEqual(h["decision"], "HANDLE")
        self.assertEqual(h["intent"], "NEW")
        self.assertEqual(h["op_status"], "OPEN")
        self.assertEqual(h["confidence"], "HIGH")
        self.assertEqual(h["ref"], "PN2606031")

    def test_services_dict(self):
        h = parse_header(SAMPLE)
        self.assertEqual(h["services"]["hotel"], "TBC")
        self.assertEqual(h["services"]["handling"], "REQUESTED")

    def test_routing_dict(self):
        h = parse_header(SAMPLE)
        self.assertEqual(h["routing"], {"ground_transport": "procurement", "hotel": "procurement"})

    def test_reason_none(self):
        h = parse_header(SAMPLE)
        self.assertEqual(h["reason"], [])

    def test_dashes_become_empty(self):
        h = parse_header("DECISION: DROP   INTENT: -   OP-STATUS: DROPPED   CONFIDENCE: HIGH   REF: -\nSERVICES: -\nROUTING: -\nREASON: -\n")
        self.assertEqual(h["services"], {})
        self.assertEqual(h["routing"], {})
        self.assertEqual(h["ref"], "-")

if __name__ == "__main__":
    unittest.main()
