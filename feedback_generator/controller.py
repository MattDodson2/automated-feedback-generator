"""Application controller, shared state, navigation and Tkinter styling."""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from .engine import FeedbackEngine
from .storage import load_templates, save_templates
from .gui.home import HomePage
from .gui.settings import SettingsPage
from .gui.template_selection import SetupSelectionPage
from .gui.template_setup import SetupPage
from .gui.scoring import MainPage
from .gui.output import OutputPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Automated Feedback Generator")
        self.geometry("1100x600")
        self.minsize(1100, 600)

        self.config_state = {
            "selected_criteria": [],
            "selected_template_name": None,
            "criteria_inputs": [],
            "grade": 0,
            "generated_feedback": None,
            "generated_versions": [],
            "current_version_index": 0,
        }

        self.template_mode = None
        self.custom_adjectives = {}
        self.feedback_engine = FeedbackEngine()
        self._mousewheel_target = None

        self.colors = {
            "bg": "#efeff0",
            "panel": "#1f2937",
            "card": "#1f2937",
            "text": "#e5e7eb",
            "muted": "#cbd5e1",
            "accent": "#4f77c4",
        }
        self.configure(bg=self.colors["bg"])

        self.templates_path = self._get_templates_path()
        self.templates = self._load_templates()
        self.feedback_engine = FeedbackEngine(custom_adjectives=self.custom_adjectives)

        self._setup_styles()

        self.container = tk.Frame(self, bg=self.colors["bg"])
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (HomePage, SetupSelectionPage, SetupPage, MainPage, OutputPage, SettingsPage):
            frame = Page(parent=self.container, controller=self, colors=self.colors)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def _get_templates_path(self) -> Path:
        # Keep the JSON data file at the project root, next to main.py.
        return Path(__file__).resolve().parent.parent / "setup_templates.json"

    def _load_templates(self) -> list[dict]:
        templates, custom_criteria, custom_adjectives, read_failed = load_templates(
            self.templates_path
        )
        self.custom_criteria = custom_criteria
        self.custom_adjectives = custom_adjectives
        if read_failed:
            messagebox.showwarning(
                "Templates file issue",
                "Your templates file could not be read. Starting with no saved templates, custom criteria, or vocabulary."
            )
        return templates

    def _save_templates(self):
        save_templates(
            self.templates_path,
            self.templates,
            self.custom_criteria,
            self.custom_adjectives,
        )

    def add_template(self, name: str, criteria: list[str]):
        existing_idx = next(
            (i for i, t in enumerate(self.templates) if t["name"].lower() == name.lower()),
            None
        )

        if existing_idx is not None:
            ok = messagebox.askyesno(
                "Overwrite template?",
                f"A template named '{name}' already exists.\n\nOverwrite it?"
            )
            if not ok:
                return False
            self.templates[existing_idx] = {"name": name, "criteria": criteria}
        else:
            self.templates.append({"name": name, "criteria": criteria})

        self.templates.sort(key=lambda t: t["name"].lower())
        self._save_templates()
        return True

    def add_custom_criterion(self, name: str):
        name = name.strip()
        if not name:
            return False

        built_in = [
            "Referencing",
            "Structure",
            "Analysis",
            "Clarity",
            "Grammar",
            "Spelling & Punctuation",
            "Critical Thinking",
            "Use of Evidence",
            "Literature Review",
            "Understanding",
            "Presentation"
        ]

        existing_names = built_in + self.custom_criteria
        if any(existing.lower() == name.lower() for existing in existing_names):
            return False

        self.custom_criteria.append(name)
        self.custom_criteria.sort(key=str.lower)
        self._save_templates()
        return True

    def add_custom_adjective(self, band: str, tone_band: str, word: str):
        band = band.strip().lower()
        tone_band = tone_band.strip().lower()
        word = word.strip()

        if band not in ("weak", "good", "excellent"):
            return False, "Invalid criterion band."

        if tone_band not in ("fail", "poor", "good", "great"):
            return False, "Invalid tone band."

        if not word:
            return False, "Please enter a word or phrase."

        existing = {
            w.lower()
            for w in self.custom_adjectives[band][tone_band]
        }

        if word.lower() in existing:
            return False, "That word already exists in this vocabulary category."

        self.custom_adjectives[band][tone_band].append(word)
        self.custom_adjectives[band][tone_band].sort(key=str.lower)
        self._save_templates()

        self.feedback_engine = FeedbackEngine(custom_adjectives=self.custom_adjectives)
        return True, "Vocabulary added successfully."

    def use_template(self, template: dict):
        self.config_state["selected_template_name"] = template["name"]
        self.config_state["selected_criteria"] = list(template["criteria"])
        self.show_frame("MainPage")

    def start_new_template(self):
        self.template_mode = "create"
        self.config_state["selected_template_name"] = None
        self.config_state["selected_criteria"] = []
        self.show_frame("SetupPage")

    def bind_mousewheel(self, canvas):
        canvas.bind("<Enter>", lambda e: self._activate_mousewheel(canvas))
        canvas.bind("<Leave>", lambda e: self._deactivate_mousewheel())

    def _activate_mousewheel(self, canvas):
        self._mousewheel_target = canvas
        self.bind_all("<MouseWheel>", self._on_global_mousewheel)

    def _deactivate_mousewheel(self):
        self._mousewheel_target = None
        self.unbind_all("<MouseWheel>")

    def _on_global_mousewheel(self, event):
        target = getattr(self, "_mousewheel_target", None)
        if target is not None and target.winfo_exists() and event.delta:
            target.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Dark.TButton",
            font=("Segoe UI", 10),
            padding=(14, 8),
            foreground=self.colors["text"],
            background=self.colors["panel"],
            borderwidth=0,
            focusthickness=0,
            focuscolor=self.colors["panel"],
        )
        style.map(
            "Dark.TButton",
            background=[("active", self.colors["card"]), ("!active", self.colors["panel"])],
            foreground=[("disabled", self.colors["muted"]), ("!disabled", self.colors["text"])],
        )

        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(18, 10),
            foreground="white",
            background=self.colors["accent"],
            borderwidth=0,
            focusthickness=0,
            focuscolor=self.colors["accent"],
        )
        style.map(
            "Accent.TButton",
            foreground=[("active", "white"), ("!active", "white")],
            background=[("active", self.colors["accent"]), ("!active", self.colors["accent"])],
        )

    def show_frame(self, page_name: str):
        frame = self.frames[page_name]

        if hasattr(frame, "refresh"):
            frame.refresh()

        frame.tkraise()
    
    def delete_template(self, template_name: str):
        original_count = len(self.templates)

        self.templates = [
            t for t in self.templates
            if t["name"].lower() != template_name.lower()
        ]

        if len(self.templates) == original_count:
            return False

        self._save_templates()
        return True

    def delete_custom_criterion(self, criterion_name: str):
        original_count = len(self.custom_criteria)

        self.custom_criteria = [
            c for c in self.custom_criteria
            if c.lower() != criterion_name.lower()
        ]

        if len(self.custom_criteria) == original_count:
            return False

        for template in self.templates:
            template["criteria"] = [
                c for c in template.get("criteria", [])
                if c.lower() != criterion_name.lower()
            ]

        self._save_templates()
        return True
