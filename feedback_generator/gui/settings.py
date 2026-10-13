"""SettingsPage GUI view (extracted from the original Tkinter application)."""

import tkinter as tk
from tkinter import ttk, messagebox


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors["bg"])
        self.controller = controller
        self.colors = colors

        self.current_section = "General"
        self.nav_buttons = {}

        header = tk.Frame(self, bg=colors["panel"], height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Settings",
            font=("Segoe UI", 16, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        ).pack(side="left", padx=20, pady=18)

        main = tk.Frame(self, bg=colors["bg"])
        main.pack(fill="both", expand=True, padx=24, pady=(20, 10))
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        side_panel = tk.Frame(main, bg=colors["panel"], width=220)
        side_panel.grid(row=0, column=0, sticky="nsw", padx=(0, 18))
        side_panel.grid_propagate(False)

        side_accent = tk.Frame(side_panel, bg=colors["accent"], height=6)
        side_accent.pack(fill="x", side="top")

        tk.Label(
            side_panel,
            text="Categories",
            font=("Segoe UI", 14, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        ).pack(anchor="w", padx=16, pady=(18, 12))

        nav_container = tk.Frame(side_panel, bg=colors["panel"])
        nav_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.sections = [
            "General",
            "Templates",
            "Criteria",
            "Vocabulary",
            "Output",
            "Advanced"
        ]

        for section in self.sections:
            btn = tk.Button(
                nav_container,
                text=section,
                font=("Segoe UI", 10, "bold" if section == self.current_section else "normal"),
                bg=colors["accent"] if section == self.current_section else colors["panel"],
                fg="white" if section == self.current_section else colors["text"],
                activebackground=colors["accent"],
                activeforeground="white",
                relief="flat",
                bd=0,
                anchor="w",
                padx=12,
                pady=10,
                command=lambda s=section: self.show_section(s)
            )
            btn.pack(fill="x", pady=4)
            self.nav_buttons[section] = btn

        content_card = tk.Frame(main, bg=colors["panel"])
        content_card.grid(row=0, column=1, sticky="nsew")
        content_card.grid_rowconfigure(1, weight=1)
        content_card.grid_columnconfigure(0, weight=1)

        content_accent = tk.Frame(content_card, bg=colors["accent"], height=6)
        content_accent.grid(row=0, column=0, sticky="ew")

        content_area = tk.Frame(content_card, bg=colors["panel"])
        content_area.grid(row=1, column=0, sticky="nsew")
        content_area.grid_rowconfigure(0, weight=1)
        content_area.grid_columnconfigure(0, weight=1)

        self.content_canvas = tk.Canvas(
            content_area,
            bg=colors["panel"],
            highlightthickness=0,
            bd=0
        )
        self.content_canvas.grid(row=0, column=0, sticky="nsew")

        content_scrollbar = ttk.Scrollbar(
            content_area,
            orient="vertical",
            command=self.content_canvas.yview
        )
        content_scrollbar.grid(row=0, column=1, sticky="ns")

        self.content_canvas.configure(yscrollcommand=content_scrollbar.set)

        self.content_inner = tk.Frame(self.content_canvas, bg=colors["panel"])
        self.content_window = self.content_canvas.create_window(
            (0, 0),
            window=self.content_inner,
            anchor="nw"
        )

        self.content_inner.bind(
            "<Configure>",
            lambda e: self.content_canvas.configure(
                scrollregion=self.content_canvas.bbox("all")
            )
        )

        self.content_canvas.bind("<Configure>", self._resize_content_window)
        self.controller.bind_mousewheel(self.content_canvas)

        bottom_bar = tk.Frame(self, bg=colors["bg"])
        bottom_bar.pack(fill="x", side="bottom", padx=24, pady=(0, 16))

        ttk.Button(
            bottom_bar,
            text="Back",
            style="Dark.TButton",
            command=lambda: controller.show_frame("HomePage")
        ).pack(side="left")

        self.show_section("General")

    def _resize_content_window(self, event):
        self.content_canvas.itemconfigure(self.content_window, width=event.width)

    def show_section(self, section_name):
        self.current_section = section_name
        self._refresh_nav_buttons()
        self._render_section_content(section_name)
        self.content_canvas.yview_moveto(0)

    def _refresh_nav_buttons(self):
        for section, btn in self.nav_buttons.items():
            is_active = section == self.current_section
            btn.config(
                bg=self.colors["accent"] if is_active else self.colors["panel"],
                fg="white" if is_active else self.colors["text"],
                font=("Segoe UI", 10, "bold" if is_active else "normal"),
            )

    def _render_section_content(self, section_name):
        for child in self.content_inner.winfo_children():
            child.destroy()

        if section_name == "Templates":
            self._render_templates_section()
            return

        if section_name == "Criteria":
            self._render_criteria_section()
            return

        if section_name == "Vocabulary":
            self._render_vocabulary_section()
            return

        tk.Label(
            self.content_inner,
            text=section_name,
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            anchor="w",
        ).pack(anchor="w", pady=(0, 10))

        placeholder_text = (
            f"This is the {section_name.lower()} settings section.\n\n"
        )

        tk.Label(
            self.content_inner,
            text=placeholder_text,
            font=("Segoe UI", 11),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            justify="left",
            anchor="nw",
            wraplength=700,
        ).pack(anchor="w")

    def _render_templates_section(self):
        tk.Label(
            self.content_inner,
            text="Templates",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            anchor="w",
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            self.content_inner,
            text="View and manage your saved templates. Use the bin icon to delete a template.",
            font=("Segoe UI", 11),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            justify="left",
            anchor="w",
            wraplength=700,
        ).pack(anchor="w", pady=(0, 18))

        templates = self.controller.templates

        if not templates:
            tk.Label(
                self.content_inner,
                text="No saved templates are currently available.",
                font=("Segoe UI", 11),
                bg=self.colors["panel"],
                fg=self.colors["muted"],
                anchor="w",
            ).pack(anchor="w")
            return

        for template in templates:
            row = tk.Frame(self.content_inner, bg=self.colors["card"])
            row.pack(fill="x", pady=6)

            info = tk.Frame(row, bg=self.colors["card"])
            info.pack(side="left", fill="x", expand=True, padx=(14, 10), pady=10)

            tk.Label(
                info,
                text=template["name"],
                font=("Segoe UI", 11, "bold"),
                bg=self.colors["card"],
                fg=self.colors["text"],
                anchor="w",
            ).pack(anchor="w")

            criteria_text = ", ".join(template.get("criteria", []))
            tk.Label(
                info,
                text=f"Criteria: {criteria_text}",
                font=("Segoe UI", 9),
                bg=self.colors["card"],
                fg=self.colors["muted"],
                anchor="w",
                wraplength=520,
                justify="left",
            ).pack(anchor="w", pady=(4, 0))

            delete_btn = tk.Button(
                row,
                text="🗑",
                font=("Segoe UI", 12),
                bg=self.colors["card"],
                fg="#fca5a5",
                activebackground=self.colors["panel"],
                activeforeground="#fecaca",
                relief="flat",
                bd=0,
                width=3,
                cursor="hand2",
                command=lambda name=template["name"]: self._confirm_delete_template(name)
            )
            delete_btn.pack(side="right", padx=12, pady=10)

    def _render_criteria_section(self):
        tk.Label(
            self.content_inner,
            text="Custom Criteria",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            anchor="w",
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            self.content_inner,
            text="View and manage your saved custom criteria. Use the bin icon to delete a criterion.",
            font=("Segoe UI", 11),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            justify="left",
            anchor="w",
            wraplength=700,
        ).pack(anchor="w", pady=(0, 18))

        criteria = self.controller.custom_criteria

        if not criteria:
            tk.Label(
                self.content_inner,
                text="No custom criteria are currently available.",
                font=("Segoe UI", 11),
                bg=self.colors["panel"],
                fg=self.colors["muted"],
                anchor="w",
            ).pack(anchor="w")
            return

        for criterion in criteria:
            row = tk.Frame(self.content_inner, bg=self.colors["card"])
            row.pack(fill="x", pady=6)

            info = tk.Frame(row, bg=self.colors["card"])
            info.pack(side="left", fill="x", expand=True, padx=(14, 10), pady=12)

            tk.Label(
                info,
                text=criterion,
                font=("Segoe UI", 11, "bold"),
                bg=self.colors["card"],
                fg=self.colors["text"],
                anchor="w",
            ).pack(anchor="w")

            usage_count = sum(
                1 for template in self.controller.templates
                if criterion in template.get("criteria", [])
            )

            tk.Label(
                info,
                text=f"Used in {usage_count} template(s)",
                font=("Segoe UI", 9),
                bg=self.colors["card"],
                fg=self.colors["muted"],
                anchor="w",
            ).pack(anchor="w", pady=(4, 0))

            delete_btn = tk.Button(
                row,
                text="🗑",
                font=("Segoe UI", 12),
                bg=self.colors["card"],
                fg="#fca5a5",
                activebackground=self.colors["panel"],
                activeforeground="#fecaca",
                relief="flat",
                bd=0,
                width=3,
                cursor="hand2",
                command=lambda name=criterion: self._confirm_delete_criterion(name)
            )
            delete_btn.pack(side="right", padx=12, pady=10)

    def _confirm_delete_template(self, template_name):
        confirmed = messagebox.askyesno(
            "Delete template",
            f"Are you sure you want to delete the template '{template_name}'?"
        )

        if not confirmed:
            return

        deleted = self.controller.delete_template(template_name)

        if deleted:
            self._render_section_content("Templates")
            self.content_canvas.yview_moveto(0)
        else:
            messagebox.showwarning(
                "Template not found",
                "The selected template could not be deleted."
            )

    def _confirm_delete_criterion(self, criterion_name):
        confirmed = messagebox.askyesno(
            "Delete custom criterion",
            (
                f"Are you sure you want to delete the custom criterion '{criterion_name}'?\n\n"
                "It will also be removed from any saved templates that use it."
            )
        )

        if not confirmed:
            return

        deleted = self.controller.delete_custom_criterion(criterion_name)

        if deleted:
            self._render_section_content("Criteria")
            self.content_canvas.yview_moveto(0)
        else:
            messagebox.showwarning(
                "Criterion not found",
                "The selected custom criterion could not be deleted."
            )

    def _render_vocabulary_section(self):
        tk.Label(
            self.content_inner,
            text="Vocabulary",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            anchor="w",
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            self.content_inner,
            text=(
                "Add your own words or short phrases to the adjective library used by the "
                "feedback engine. Choose the performance band and tone band, then save the word."
            ),
            font=("Segoe UI", 11),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            justify="left",
            anchor="w",
            wraplength=700,
        ).pack(anchor="w", pady=(0, 18))

        form_card = tk.Frame(self.content_inner, bg=self.colors["card"])
        form_card.pack(fill="x", pady=(0, 18))

        form_inner = tk.Frame(form_card, bg=self.colors["card"])
        form_inner.pack(fill="x", padx=16, pady=16)

        tk.Label(
            form_inner,
            text="Criterion band",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        band_var = tk.StringVar(value="weak")
        band_box = ttk.Combobox(
            form_inner,
            textvariable=band_var,
            values=["weak", "good", "excellent"],
            state="readonly",
            width=18
        )
        band_box.grid(row=1, column=0, sticky="w", padx=(0, 18), pady=(0, 14))

        tk.Label(
            form_inner,
            text="Tone band",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            anchor="w",
        ).grid(row=0, column=1, sticky="w", pady=(0, 6))

        tone_var = tk.StringVar(value="fail")
        tone_box = ttk.Combobox(
            form_inner,
            textvariable=tone_var,
            values=["fail", "poor", "good", "great"],
            state="readonly",
            width=18
        )
        tone_box.grid(row=1, column=1, sticky="w", pady=(0, 14))

        tk.Label(
            form_inner,
            text="Word or phrase",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            anchor="w",
        ).grid(row=2, column=0, sticky="w", pady=(0, 6))

        word_entry = tk.Entry(
            form_inner,
            font=("Segoe UI", 10),
            width=40
        )
        word_entry.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 14))
        word_entry.focus_set()

        def save_word():
            band = band_var.get()
            tone = tone_var.get()
            word = word_entry.get().strip()

            success, message = self.controller.add_custom_adjective(band, tone, word)

            if success:
                messagebox.showinfo("Saved", message)
                self.show_section("Vocabulary")
            else:
                messagebox.showwarning("Could not save", message)

        ttk.Button(
            form_inner,
            text="Add to Vocabulary",
            style="Accent.TButton",
            command=save_word
        ).grid(row=4, column=0, sticky="w")

        vocabulary = self.controller.custom_adjectives

        tk.Label(
            self.content_inner,
            text="Current custom vocabulary",
            font=("Segoe UI", 13, "bold"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            anchor="w",
        ).pack(anchor="w", pady=(4, 10))

        for band in ("weak", "good", "excellent"):
            band_card = tk.Frame(self.content_inner, bg=self.colors["card"])
            band_card.pack(fill="x", pady=6)

            band_inner = tk.Frame(band_card, bg=self.colors["card"])
            band_inner.pack(fill="x", padx=14, pady=12)

            tk.Label(
                band_inner,
                text=band.capitalize(),
                font=("Segoe UI", 11, "bold"),
                bg=self.colors["card"],
                fg=self.colors["text"],
                anchor="w",
            ).pack(anchor="w", pady=(0, 8))

            for tone in ("fail", "poor", "good", "great"):
                words = vocabulary.get(band, {}).get(tone, [])
                display_text = ", ".join(words) if words else "No custom words added"

                tk.Label(
                    band_inner,
                    text=f"{tone.capitalize()}: {display_text}",
                    font=("Segoe UI", 9),
                    bg=self.colors["card"],
                    fg=self.colors["muted"],
                    justify="left",
                    anchor="w",
                    wraplength=650,
                ).pack(anchor="w", pady=2)

    def refresh(self):
        self.show_section(self.current_section)
