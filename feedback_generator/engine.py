"""Rule-based feedback generation, independent of the Tkinter GUI."""

import random


class FeedbackEngine:
    def __init__(self, custom_adjectives=None):
        self.frames = {
            "strength": [
                "Your {criterion} {verb} {adjective}.",
                "One aspect of the work worth highlighting is its {criterion}, which {verb} {adjective}.",
                "The quality of the work's {criterion} is {adjective}."
            ],
            "improvement": [
                "Your {criterion} {verb} {adjective} and would benefit from further development.",
                "An area that needs improvement is {criterion}, which {verb} currently {adjective}.",
                "The {criterion} {verb} {adjective} and could be strengthened further."
            ]
        }

        self.default_adjectives = {
            "weak": {
                "fail": ["very limited", "underdeveloped", "unclear"],
                "poor": ["basic", "inconsistent", "partially developed"],
                "good": ["limited", "uncertain", "underdeveloped"],
                "great": ["uneven", "inconsistent", "not yet secure"]
            },
            "good": {
                "fail": ["adequate in parts", "occasionally clear", "partially effective"],
                "poor": ["developing", "reasonably clear", "competent in parts"],
                "good": ["competent", "clear", "generally effective"],
                "great": ["solid", "well-developed", "effective"]
            },
            "excellent": {
                "fail": ["clear in places", "effective in parts", "strong at points"],
                "poor": ["strong", "effective", "well-executed"],
                "good": ["strong", "effective", "well-executed"],
                "great": ["excellent", "highly effective", "particularly strong"]
            }
        }

        self.custom_adjectives = custom_adjectives if custom_adjectives is not None else {
            "weak": {"fail": [], "poor": [], "good": [], "great": []},
            "good": {"fail": [], "poor": [], "good": [], "great": []},
            "excellent": {"fail": [], "poor": [], "good": [], "great": []},
        }

        self.criterion_labels = {
            "Referencing": "referencing",
            "Structure": "structure",
            "Analysis": "analysis",
            "Clarity": "clarity",
            "Grammar": "written accuracy",
            "Spelling & Punctuation": "spelling and punctuation",
            "Critical Thinking": "critical thinking",
            "Use of Evidence": "use of evidence",
            "Literature Review": "literature review",
            "Understanding": "understanding",
            "Presentation": "presentation"
        }

        self.comment_frames = {
            "weak": [
                " {comment}",
                " In particular, {comment}",
                " This is shown by {comment}"
            ],
            "good": [
                " {comment}",
                " At points, {comment}",
                " This can be seen in {comment}"
            ],
            "excellent": [
                " {comment}",
                " In particular, {comment}",
                " This is evident in {comment}"
            ]
        }

    def generate_feedback(self, criteria_inputs, grade, used_tracker=None):
        validated = self._validate_inputs(criteria_inputs, grade)
        tone_band = self._grade_to_tone_band(grade)

        annotated = []
        for item in validated:
            annotated.append({
                "criterion": item["criterion"],
                "score": item["score"],
                "comment": item["comment"],
                "band": self._score_to_band(item["score"]),
            })

        selected = self._select_key_criteria(annotated)

        strength_items = [item for item in selected if item["band"] == "excellent"]
        improvement_items = [item for item in selected if item["band"] in ("weak", "good")]

        strength_sentences = [
            self._build_criterion_sentence(item, tone_band, used_tracker)
            for item in strength_items
        ]

        improvement_sentences = [
            self._build_criterion_sentence(item, tone_band, used_tracker)
            for item in improvement_items
        ]

        grade_summary = self._grade_to_summary(grade)
        closing_line = self._grade_to_closing(grade)

        parts = [grade_summary]
        parts.extend(strength_sentences)
        parts.extend(improvement_sentences)
        parts.append(closing_line)

        final_feedback = "\n\n".join(part for part in parts if part.strip())

        return {
            "grade": grade,
            "tone_band": tone_band,
            "selected_criteria": selected,
            "strength_sentences": strength_sentences,
            "improvement_sentences": improvement_sentences,
            "grade_summary": grade_summary,
            "closing_line": closing_line,
            "final_feedback": final_feedback,
        }

    def generate_multiple_feedback(self, criteria_inputs, grade, count=3):
        versions = []
        seen_feedback = set()
        used_tracker = {}
        max_attempts = count * 10

        attempts = 0
        while len(versions) < count and attempts < max_attempts:
            result = self.generate_feedback(
                criteria_inputs,
                grade,
                used_tracker=used_tracker
            )

            feedback_text = result["final_feedback"].strip()

            if feedback_text not in seen_feedback:
                versions.append(result)
                seen_feedback.add(feedback_text)

            attempts += 1

        if not versions:
            raise ValueError("No feedback versions could be generated.")

        return versions

    def _validate_inputs(self, criteria_inputs, grade):
        if not isinstance(criteria_inputs, list):
            raise ValueError("criteria_inputs must be a list.")

        cleaned = []

        for item in criteria_inputs:
            if not isinstance(item, dict):
                continue

            criterion = str(item.get("criterion", "")).strip()
            score = item.get("score")
            comment = str(item.get("comment", "")).strip()

            if not criterion:
                continue

            if not isinstance(score, int):
                continue

            if score < 1 or score > 5:
                continue

            cleaned.append({
                "criterion": criterion,
                "score": score,
                "comment": comment,
            })

        if not cleaned:
            raise ValueError("No valid criterion inputs were provided.")

        if not isinstance(grade, int):
            raise ValueError("grade must be an integer.")

        allowed_grades = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100}

        if grade not in allowed_grades:
            raise ValueError("grade must be in increments of 10 from 0 to 100.")

        return cleaned

    def _score_to_band(self, score):
        if score in (1, 2):
            return "weak"

        if score == 3:
            return "good"

        return "excellent"

    def _grade_to_tone_band(self, grade):
        if grade in (0, 10, 20, 30):
            return "fail"

        if grade in (40, 50):
            return "poor"

        if grade == 60:
            return "good"

        return "great"

    def _select_key_criteria(self, annotated_inputs):
        if len(annotated_inputs) <= 3:
            return annotated_inputs

        indexed = list(enumerate(annotated_inputs))

        lowest_two = sorted(
            indexed,
            key=lambda pair: (pair[1]["score"], pair[0])
        )[:2]

        highest_one = sorted(
            indexed,
            key=lambda pair: (-pair[1]["score"], pair[0])
        )[:1]

        chosen_indices = []

        for idx, _ in lowest_two + highest_one:
            if idx not in chosen_indices:
                chosen_indices.append(idx)

        selected = [annotated_inputs[idx] for idx in chosen_indices]

        if len(selected) < 3:
            for idx, item in indexed:
                if idx not in chosen_indices:
                    selected.append(item)
                    chosen_indices.append(idx)

                if len(selected) == 3:
                    break

        return selected

    def _build_criterion_sentence(self, item, tone_band, used_tracker=None):
        criterion = item["criterion"]
        band = item["band"]
        comment = item["comment"]

        frame_type = self._band_to_frame_type(band)
        criterion_text = self.criterion_labels.get(criterion, criterion.lower())

        frame = self._choose_from_library(
            library=self.frames[frame_type],
            key=("frame", frame_type),
            used_tracker=used_tracker
        )

        adjective_library = self._get_adjective_library(band, tone_band)

        adjective = self._choose_from_library(
            library=adjective_library,
            key=("adjective", band, tone_band),
            used_tracker=used_tracker
        )

        # The built-in "Spelling & Punctuation" label has a compound plural subject.
        # Use predicative adjective frames rather than "a/an {adjective}" so both
        # ordinary and user-configured multi-word descriptions read naturally.
        verb = "are" if criterion_text == "spelling and punctuation" else "is"
        sentence = frame.format(
            criterion=criterion_text,
            adjective=adjective,
            verb=verb,
        )

        if criterion == "Analysis" and comment:
            comment_frame = self._choose_from_library(
                library=self.comment_frames[band],
                key=("comment_frame", band),
                used_tracker=used_tracker
            )

            sentence += comment_frame.format(comment=comment)

        return sentence

    def _get_adjective_library(self, band, tone_band):
        custom_words = self.custom_adjectives.get(band, {}).get(tone_band, [])
        default_words = self.default_adjectives.get(band, {}).get(tone_band, [])

        seen = set()
        combined = []

        for word in custom_words:
            clean = str(word).strip()
            if clean and clean.lower() not in seen:
                combined.append(clean)
                seen.add(clean.lower())

        for word in default_words:
            clean = str(word).strip()
            if clean and clean.lower() not in seen:
                combined.append(clean)
                seen.add(clean.lower())

        return combined

    def _band_to_frame_type(self, band):
        if band == "excellent":
            return "strength"

        return "improvement"

    def _choose_from_library(self, library, key, used_tracker=None):
        if not library:
            raise ValueError(f"No language options available for {key}.")

        if used_tracker is None:
            return random.choice(library)

        already_used = used_tracker.setdefault(key, [])
        available = [item for item in library if item not in already_used]

        if available:
            choice = random.choice(available)
            already_used.append(choice)
            return choice

        choice = random.choice(library)
        already_used.append(choice)
        return choice

    def _grade_to_summary(self, grade):
        if grade in (0, 10, 20, 30):
            return (
                "This work shows some level of understanding but it remains below the expected standard "
                "and requires significant development across key areas."
            )

        if grade in (40, 50):
            return (
                "This work demonstrates a limited but developing standard, with some clear strengths as well "
                "as areas that need further improvement."
            )

        if grade == 60:
            return (
                "This work demonstrates a good overall standard, with several effective features across the "
                "selected criteria."
            )

        return (
            "This work demonstrates a very strong overall standard, with clear evidence of achievement across "
            "the selected criteria."
        )

    def _grade_to_closing(self, grade):
        if grade in (0, 10, 20, 30):
            return (
                "Focusing on the areas identified above would help strengthen the overall quality of the work."
            )

        if grade in (40, 50):
            return (
                "With further development in the weaker areas, the overall standard of the work could be improved."
            )

        if grade == 60:
            return (
                "Continued refinement of the areas identified would help develop this work further."
            )

        return (
            "Refining the smaller areas identified above would help strengthen an already very effective response."
        )
