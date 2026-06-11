import unittest
from check_consistency import run_checks

class TestConsistency(unittest.TestCase):
    def test_returns_dict_with_zero_failures(self):
        result = run_checks()
        # result: check keys → real-system-refs, icao_coverage, stale_paths (all empty lists when clean)
        self.assertIsInstance(result, dict)
        problems = {k: v for k, v in result.items() if v}
        self.assertEqual(problems, {}, f"consistency problems: {problems}")

if __name__ == "__main__":
    unittest.main()
