# Structural refactor: what changed

This is the first, **behaviour-preserving** imporvememt I made to the program following my original dissertation submission.

## Before

- `FrameBasedVersion.py` (2,479 lines) defined the application controller, six Tkinter pages, feedback engine and persistence functions in one file.
- `setup_templates.json` stored local settings and assessment templates alongside the script.

## After

- `main.py` is the small application entry point.
- `feedback_generator/controller.py` contains the `App` controller, shared configuration state, navigation and UI styling.
- `feedback_generator/gui/` contains the six page classes, in separate modules.
- `feedback_generator/engine.py` contains `FeedbackEngine` independently of Tkinter.
- `feedback_generator/storage.py` handles the original JSON format and returns a read-error flag for the controller to display warnings. It does not depend on the GUI.
- `setup_templates.json` stays at project root for backward compatibility with saved templates, but is excluded from Git; `setup_templates.example.json` documents the data format.

## What didn't change

- The generated feedback logic and wording.
- Existing GUI screen layouts and navigation.
- Existing interface limitations which are outlined in `README.md`.

## Checks performed for this refactor

- All Python modules compiled successfully.
- Engine output compared with the original implementation under 54 seeded scenarios with identical results.
- The original JSON format successfully loaded and round-tripped through the new storage module; missing and malformed JSON conditions were checked.
- Under a virtual display, both the original and refactored GUI instantiated all six pages, navigated between screens and generated identical feedback for the same inputs.

These are targeted smoke and equivalence checks, not a complete automated test suite.

## How to run

From the repository root:

```bash
python main.py
```

On some Linux installations, Tkinter is distributed separately as `python3-tk`.
