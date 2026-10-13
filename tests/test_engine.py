"""Behavioural unit tests for the feedback engine (no Tkinter required)."""

import random
import unittest
from unittest.mock import patch

from feedback_generator.engine import FeedbackEngine


class TestInputValidation(unittest.TestCase):
    def setUp(self):
        self.engine = FeedbackEngine()

    def test_accepts_valid_scores_and_trims_input(self):
        supplied = [
            {"criterion": " Analysis ", "score": 4, "comment": "  Specific example.  "},
            {"criterion": "Structure", "score": 1},
        ]
        self.assertEqual(self.engine._validate_inputs(supplied, 70), [
            {"criterion": "Analysis", "score": 4, "comment": "Specific example."},
            {"criterion": "Structure", "score": 1, "comment": ""},
        ])

    def test_ignores_invalid_criteria_if_valid_ones_remain(self):
        supplied = [
            None,
            {"criterion": "", "score": 3},
            {"criterion": "Clarity", "score": 0},
            {"criterion": "Grammar", "score": 6},
            {"criterion": "Analysis", "score": "3"},
            {"criterion": "Structure", "score": 2},
        ]
        self.assertEqual(self.engine._validate_inputs(supplied, 40), [
            {"criterion": "Structure", "score": 2, "comment": ""}
        ])

    def test_rejects_non_list_input(self):
        with self.assertRaisesRegex(ValueError, "must be a list"):
            self.engine._validate_inputs({}, 60)

    def test_rejects_inputs_with_no_valid_criteria(self):
        with self.assertRaisesRegex(ValueError, "No valid criterion"):
            self.engine._validate_inputs([{"criterion": "Analysis", "score": 8}], 60)

    def test_rejects_invalid_grade_types_and_boundaries(self):
        inputs = [{"criterion": "Analysis", "score": 3}]
        for grade in (45, -10, 110, 60.0, "60"):
            with self.subTest(grade=grade), self.assertRaises(ValueError):
                self.engine._validate_inputs(inputs, grade)

    def test_grade_extremes_are_accepted(self):
        inputs = [{"criterion": "Analysis", "score": 3}]
        for grade in (0, 100):
            with self.subTest(grade=grade):
                self.assertEqual(len(self.engine._validate_inputs(inputs, grade)), 1)


class TestSelectionRules(unittest.TestCase):
    def setUp(self):
        self.engine = FeedbackEngine()

    def test_score_bands(self):
        expected = {1: "weak", 2: "weak", 3: "good", 4: "excellent", 5: "excellent"}
        for score, band in expected.items():
            with self.subTest(score=score):
                self.assertEqual(self.engine._score_to_band(score), band)

    def test_grade_to_tone_bands(self):
        expected = {
            0: "fail", 10: "fail", 20: "fail", 30: "fail",
            40: "poor", 50: "poor", 60: "good",
            70: "great", 80: "great", 90: "great", 100: "great",
        }
        for grade, tone in expected.items():
            with self.subTest(grade=grade):
                self.assertEqual(self.engine._grade_to_tone_band(grade), tone)

    def test_uses_all_criteria_when_three_or_fewer(self):
        for size in (1, 2, 3):
            supplied = [{"criterion": f"C{i}", "score": i + 1} for i in range(size)]
            with self.subTest(size=size):
                self.assertEqual(self.engine._select_key_criteria(supplied), supplied)

    def test_four_or_more_selects_two_lowest_and_one_highest(self):
        supplied = [
            {"criterion": "One", "score": 3},
            {"criterion": "Two", "score": 1},
            {"criterion": "Three", "score": 5},
            {"criterion": "Four", "score": 2},
            {"criterion": "Five", "score": 4},
        ]
        selected = self.engine._select_key_criteria(supplied)
        self.assertEqual([i["criterion"] for i in selected], ["Two", "Four", "Three"])
        self.assertEqual(len(selected), 3)

    def test_ties_have_stable_input_order_and_no_duplicates(self):
        supplied = [
            {"criterion": "First", "score": 3},
            {"criterion": "Second", "score": 3},
            {"criterion": "Third", "score": 3},
            {"criterion": "Fourth", "score": 3},
        ]
        chosen = self.engine._select_key_criteria(supplied)
        self.assertEqual([item["criterion"] for item in chosen], ["First", "Second", "Third"])


class TestLanguageLibraries(unittest.TestCase):
    def setUp(self):
        self.engine = FeedbackEngine()

    def test_custom_adjectives_are_first_and_case_insensitive_duplicates_removed(self):
        custom = {
            "excellent": {"great": [" Excellent ", "exceptional", "EXCEPTIONAL"]}
        }
        engine = FeedbackEngine(custom_adjectives=custom)
        self.assertEqual(
            engine._get_adjective_library("excellent", "great"),
            ["Excellent", "exceptional", "highly effective", "particularly strong"],
        )

    def test_used_tracker_prefers_unused_options_before_repeating(self):
        tracker = {}
        with patch("feedback_generator.engine.random.choice", side_effect=lambda choices: choices[0]):
            selections = [
                self.engine._choose_from_library(["a", "b", "c"], ("frame", "strength"), tracker)
                for _ in range(4)
            ]
        self.assertEqual(selections, ["a", "b", "c", "a"])

    def test_empty_library_rejected(self):
        with self.assertRaisesRegex(ValueError, "No language options"):
            self.engine._choose_from_library([], ("empty",))

    def test_strength_and_improvement_frames(self):
        self.assertEqual(self.engine._band_to_frame_type("excellent"), "strength")
        self.assertEqual(self.engine._band_to_frame_type("weak"), "improvement")
        self.assertEqual(self.engine._band_to_frame_type("good"), "improvement")


class TestGrammaticalSentenceFrames(unittest.TestCase):
    """Catch agreement and article errors in generated criterion sentences."""

    def setUp(self):
        self.engine = FeedbackEngine()

    def render(self, criterion, band, frame, adjective):
        item = {"criterion": criterion, "band": band, "comment": ""}
        with patch.object(
            self.engine,
            "_choose_from_library",
            side_effect=[frame, adjective],
        ):
            return self.engine._build_criterion_sentence(item, "great")

    def test_all_strength_frames_support_vowel_and_consonant_adjectives(self):
        words = ["excellent", "effective", "outstanding", "particularly strong"]
        for frame in self.engine.frames["strength"]:
            for word in words:
                with self.subTest(frame=frame, adjective=word):
                    sentence = self.render("Analysis", "excellent", frame, word)
                    self.assertIn(word, sentence)
                    self.assertIn("analysis", sentence)
                    self.assertNotIn("a " + word, sentence.lower())
                    self.assertNotIn("an " + word, sentence.lower())
                    self.assertTrue(sentence.endswith("."))

    def test_qualifying_adjective_phrases_are_not_used_before_nouns(self):
        phrases = ["clear in places", "effective in parts", "strong at points"]
        for frame in self.engine.frames["strength"]:
            for phrase in phrases:
                with self.subTest(frame=frame, phrase=phrase):
                    sentence = self.render("Analysis", "excellent", frame, phrase)
                    self.assertIn(" " + phrase, sentence)
                    self.assertNotIn(phrase + " aspect", sentence)
                    self.assertNotIn(phrase + " standard", sentence)

    def test_compound_spelling_and_punctuation_uses_plural_agreement(self):
        for band, adjectives in [
            ("excellent", "excellent"),
            ("good", "competent"),
            ("weak", "inconsistent"),
        ]:
            frame_type = "strength" if band == "excellent" else "improvement"
            for frame in self.engine.frames[frame_type]:
                with self.subTest(band=band, frame=frame):
                    sentence = self.render("Spelling & Punctuation", band, frame, adjectives)
                    self.assertIn("spelling and punctuation", sentence)
                    # The possessive-quality frame has a singular subject: quality.
                    if "{verb}" in frame:
                        self.assertIn(" are ", sentence)
                        self.assertNotIn("punctuation is", sentence)
                        self.assertNotIn("which is", sentence)

    def test_singular_criteria_still_use_singular_agreement(self):
        for band in ("excellent", "good", "weak"):
            frame_type = "strength" if band == "excellent" else "improvement"
            for frame in self.engine.frames[frame_type]:
                with self.subTest(band=band, frame=frame):
                    sentence = self.render("Analysis", band, frame, "clear")
                    if "{verb}" in frame:
                        self.assertIn(" is ", sentence)


class TestFeedbackGeneration(unittest.TestCase):
    def setUp(self):
        self.engine = FeedbackEngine()
        self.criteria = [
            {"criterion": "Analysis", "score": 5, "comment": "good examples."},
            {"criterion": "Structure", "score": 2, "comment": ""},
            {"criterion": "Clarity", "score": 3, "comment": ""},
            {"criterion": "Referencing", "score": 4, "comment": ""},
        ]

    def test_feedback_contains_expected_parts_in_order(self):
        with patch("feedback_generator.engine.random.choice", side_effect=lambda items: items[0]):
            result = self.engine.generate_feedback(self.criteria, 70)
        self.assertEqual(result["grade"], 70)
        self.assertEqual(result["tone_band"], "great")
        self.assertEqual([x["criterion"] for x in result["selected_criteria"]],
                         ["Structure", "Clarity", "Analysis"])
        self.assertEqual(len(result["strength_sentences"]), 1)
        self.assertEqual(len(result["improvement_sentences"]), 2)
        self.assertTrue(result["final_feedback"].startswith(result["grade_summary"]))
        self.assertTrue(result["final_feedback"].endswith(result["closing_line"]))
        self.assertIn("good examples.", result["final_feedback"])

    def test_generated_summary_and_closing_depend_on_grade(self):
        with patch("feedback_generator.engine.random.choice", side_effect=lambda items: items[0]):
            low = self.engine.generate_feedback(self.criteria[:1], 20)
            high = self.engine.generate_feedback(self.criteria[:1], 80)
        self.assertNotEqual(low["grade_summary"], high["grade_summary"])
        self.assertNotEqual(low["closing_line"], high["closing_line"])

    def test_seed_reproduces_wording_in_current_random_implementation(self):
        state = random.getstate()
        try:
            random.seed(1234)
            one = self.engine.generate_feedback(self.criteria, 70)
            random.seed(1234)
            two = self.engine.generate_feedback(self.criteria, 70)
            self.assertEqual(one, two)
        finally:
            random.setstate(state)

    def test_generates_multiple_distinct_versions_for_typical_input(self):
        state = random.getstate()
        try:
            random.seed(12)
            versions = self.engine.generate_multiple_feedback(self.criteria, 70, count=3)
        finally:
            random.setstate(state)
        self.assertEqual(len(versions), 3)
        self.assertEqual(len({v["final_feedback"] for v in versions}), 3)

    def test_non_positive_count_raises_no_versions_error(self):
        with self.assertRaisesRegex(ValueError, "No feedback versions"):
            self.engine.generate_multiple_feedback(self.criteria[:1], 60, count=0)


if __name__ == "__main__":
    unittest.main()
