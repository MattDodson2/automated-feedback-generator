"""Read and write local template data without depending on the user interface."""

import json
from pathlib import Path


def empty_custom_adjectives() -> dict:
    """Return a fresh copy of the original three-band vocabulary structure."""
    return {
        "weak": {"fail": [], "poor": [], "good": [], "great": []},
        "good": {"fail": [], "poor": [], "good": [], "great": []},
        "excellent": {"fail": [], "poor": [], "good": [], "great": []},
    }


def load_templates(path: Path) -> tuple[list[dict], list[str], dict, bool]:
    """Return (templates, custom criteria, vocabulary, read_failed).

    Preserves the original loader's validation and fallback behaviour.
    The controller handles displaying any warning to the user.
    """
    custom_criteria = []
    custom_adjectives = empty_custom_adjectives()

    if not path.exists():
        return [], custom_criteria, custom_adjectives, False

    try:
        data = json.loads(path.read_text(encoding="utf-8"))

        templates = data.get("templates", [])
        clean_templates = []

        if isinstance(templates, list):
            for t in templates:
                if isinstance(t, dict) and "name" in t and "criteria" in t:
                    if isinstance(t["criteria"], list):
                        clean_templates.append({
                            "name": str(t["name"]),
                            "criteria": [str(c) for c in t["criteria"]]
                        })

        custom_criteria = data.get("custom_criteria", [])
        if isinstance(custom_criteria, list):
            clean_custom = []
            for item in custom_criteria:
                name = str(item).strip()
                if name and name.lower() not in [c.lower() for c in clean_custom]:
                    clean_custom.append(name)
            custom_criteria = sorted(clean_custom, key=str.lower)
        else:
            custom_criteria = []

        custom_adjectives = data.get("custom_adjectives", {})
        clean_adjectives = empty_custom_adjectives()
        if isinstance(custom_adjectives, dict):
            for band in ("weak", "good", "excellent"):
                band_data = custom_adjectives.get(band, {})
                if not isinstance(band_data, dict):
                    continue

                for tone in ("fail", "poor", "good", "great"):
                    words = band_data.get(tone, [])
                    if isinstance(words, list):
                        clean_words = []
                        seen = set()
                        for word in words:
                            clean_word = str(word).strip()
                            if clean_word and clean_word.lower() not in seen:
                                clean_words.append(clean_word)
                                seen.add(clean_word.lower())
                        clean_adjectives[band][tone] = clean_words

        return clean_templates, custom_criteria, clean_adjectives, False

    except Exception:
        return [], [], empty_custom_adjectives(), True


def save_templates(path: Path, templates: list[dict], custom_criteria: list[str], custom_adjectives: dict) -> None:
    """Write data in the same JSON shape and indentation as the original."""
    payload = {
        "templates": templates,
        "custom_criteria": custom_criteria,
        "custom_adjectives": custom_adjectives,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
