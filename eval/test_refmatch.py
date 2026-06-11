import unittest
from refmatch import ref_ok

class TestRefMatch(unittest.TestCase):
    def test_assign_accepts_rendered_pn(self):
        self.assertTrue(ref_ok("assign", "PN2606031"))
    def test_assign_accepts_placeholder(self):
        self.assertTrue(ref_ok("assign", "{{ASSIGN:PN2606-031}}"))
    def test_assign_rejects_garbage(self):
        self.assertFalse(ref_ok("assign", "TRIP-7"))
    def test_fixed_requires_exact(self):
        self.assertTrue(ref_ok("fixed:PN2606014", "PN2606014"))
        self.assertFalse(ref_ok("fixed:PN2606014", "PN2606099"))
    def test_dash_for_drop(self):
        self.assertTrue(ref_ok("none", "-"))
        self.assertFalse(ref_ok("none", "PN2606014"))

if __name__ == "__main__":
    unittest.main()
