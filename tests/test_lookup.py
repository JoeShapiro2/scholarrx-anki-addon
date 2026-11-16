import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lookup", ROOT / "scholarrx" / "lookup.py")
lookup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lookup)


class LookupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping = lookup.load_mapping(ROOT / "scholarrx" / "mapping.json")

    def test_separators_trailing_comma_and_duplicates(self):
        self.assertEqual(lookup.parse_qids("1171.21, 1175.21\n1171.21,\t,"), ["1171.21", "1175.21"])

    def test_preserves_full_identifier(self):
        self.assertEqual(lookup.parse_qids("001.21 1171.21 1171.22"), ["001.21", "1171.21", "1171.22"])

    def test_empty_and_invalid(self):
        for text in ("", ", ,\n", "1171.21 OR", "1171.21;1175.21", "1171..21"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                lookup.parse_qids(text)

    def test_known_question(self):
        query, missing = lookup.lookup(["1171.21"], self.mapping)
        self.assertEqual(missing, [])
        self.assertEqual(query.count("ankihub_id:"), 11)
        self.assertIn("ankihub_id:32869230-ea5b-4ea2-8510-a7bc407d1f70", query)

    def test_partial_unknown(self):
        query, missing = lookup.lookup(["1171.21", "99999999.99"], self.mapping)
        self.assertTrue(query)
        self.assertEqual(missing, ["99999999.99"])

    def test_all_unknown_never_searches_all_cards(self):
        self.assertEqual(lookup.lookup(["99999999.99"], self.mapping), ("", ["99999999.99"]))

    def test_repeated_notes_are_deduplicated(self):
        query, _ = lookup.lookup(["1171.21", "1171.21"], self.mapping)
        self.assertEqual(query.count("ankihub_id:"), 11)

    def test_weak_matches_included(self):
        weak = [qid for qid, entry in self.mapping.items() if entry["quality"] == "Weak - best guesses"]
        self.assertEqual(len(weak), 66)
        for qid in weak:
            query, missing = lookup.lookup([qid], self.mapping)
            self.assertTrue(query)
            self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
