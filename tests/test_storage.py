"""Unit tests for JSON configuration persistence using temporary files only."""

import json
import tempfile
import unittest
from pathlib import Path

from feedback_generator.storage import (
    empty_custom_adjectives,
    load_templates,
    save_templates,
)


class TestTemplateStorage(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.file = Path(self.tmpdir.name) / "setup_templates.json"

    def test_fresh_adjective_structures_are_independent(self):
        first = empty_custom_adjectives()
        second = empty_custom_adjectives()
        self.assertEqual(set(first), {"weak", "good", "excellent"})
        self.assertEqual(set(first["weak"]), {"fail", "poor", "good", "great"})
        first["weak"]["fail"].append("added")
        self.assertEqual(second["weak"]["fail"], [])

    def test_missing_file_returns_defaults_without_warning(self):
        self.assertEqual(load_templates(self.file), ([], [], empty_custom_adjectives(), False))

    def test_reads_valid_data_and_normalises_custom_values(self):
        payload = {
            "templates": [
                {"name": "Essay", "criteria": ["Analysis", "Structure"]},
                {"name": "Mixed", "criteria": [1, "Clarity"]},
                {"name": "No list", "criteria": "Analysis"},
                "not a template",
            ],
            "custom_criteria": [" creative writing ", "CREATIVE WRITING", "Physics", "", "physics"],
            "custom_adjectives": {
                "weak": {"fail": [" hesitant ", "HESITANT", "vague", ""]},
                "excellent": {"great": [" outstanding "]},
            },
        }
        self.file.write_text(json.dumps(payload), encoding="utf-8")
        templates, criteria, adjectives, warning = load_templates(self.file)
        self.assertFalse(warning)
        self.assertEqual(templates, [
            {"name": "Essay", "criteria": ["Analysis", "Structure"]},
            {"name": "Mixed", "criteria": ["1", "Clarity"]},
        ])
        self.assertEqual(criteria, ["creative writing", "Physics"])
        self.assertEqual(adjectives["weak"]["fail"], ["hesitant", "vague"])
        self.assertEqual(adjectives["excellent"]["great"], ["outstanding"])
        self.assertEqual(adjectives["good"]["poor"], [])

    def test_ignores_wrong_section_types(self):
        self.file.write_text(json.dumps({
            "templates": "wrong",
            "custom_criteria": {},
            "custom_adjectives": ["wrong"],
        }), encoding="utf-8")
        self.assertEqual(load_templates(self.file), ([], [], empty_custom_adjectives(), False))

    def test_malformed_json_recovers_defaults_and_flags_warning(self):
        self.file.write_text("{ invalid JSON", encoding="utf-8")
        self.assertEqual(load_templates(self.file), ([], [], empty_custom_adjectives(), True))

    def test_invalid_top_level_json_flags_warning(self):
        self.file.write_text("[]", encoding="utf-8")
        self.assertEqual(load_templates(self.file), ([], [], empty_custom_adjectives(), True))

    def test_directory_instead_of_file_flags_warning(self):
        self.file.mkdir()
        self.assertEqual(load_templates(self.file), ([], [], empty_custom_adjectives(), True))

    def test_round_trip_preserves_saved_template_data(self):
        templates = [{"name": "Science", "criteria": ["Analysis", "Evidence"]}]
        criteria = ["Evidence"]
        adjectives = empty_custom_adjectives()
        adjectives["excellent"]["great"] = ["exceptional"]
        save_templates(self.file, templates, criteria, adjectives)
        self.assertEqual(load_templates(self.file), (templates, criteria, adjectives, False))
        self.assertEqual(set(json.loads(self.file.read_text(encoding="utf-8"))),
                         {"templates", "custom_criteria", "custom_adjectives"})

    def test_sample_configuration_can_be_loaded(self):
        sample = Path(__file__).resolve().parents[1] / "setup_templates.example.json"
        templates, criteria, adjectives, warning = load_templates(sample)
        self.assertFalse(warning)
        self.assertEqual(templates[0]["name"], "Example assessment")
        self.assertEqual(criteria, [])
        self.assertEqual(adjectives, empty_custom_adjectives())

    def test_save_propagates_write_failure(self):
        missing_parent = Path(self.tmpdir.name) / "missing" / "data.json"
        with self.assertRaises(FileNotFoundError):
            save_templates(missing_parent, [], [], empty_custom_adjectives())


if __name__ == "__main__":
    unittest.main()
