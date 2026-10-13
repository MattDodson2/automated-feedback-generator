"""SetupPage GUI view (extracted from the original Tkinter application)."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class SetupPage(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors["bg"])
        self.controller = controller
        self.colors = colors

        self.available_criteria = [
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

        self.criteria_vars = {}

        header = tk.Frame(self, bg=colors["panel"], height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        header_title = tk.Label(
            header,
            text="Setup: Choose Criteria",
            font=("Segoe UI", 16, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        )
        header_title.pack(side="left", padx=20)

        main = tk.Frame(self, bg=colors["bg"])
        main.pack(fill="both", expand=True)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)

        card = tk.Frame(main, bg=colors["card"])
        card.grid(row=0, column=0, padx=40, pady=40, sticky="n")

        accent = tk.Frame(card, bg=colors["accent"], height=6)
        accent.pack(fill="x", side="top")

        inner = tk.Frame(card, bg=colors["card"])
        inner.pack(fill="both", expand=True, padx=40, pady=24)

        inner.grid_columnconfigure(0, weight=1)
        inner.grid_rowconfigure(2, weight=1)

        title = tk.Label(
            inner,
            text="Select the criteria you want to assess",
            font=("Segoe UI", 18, "bold"),
            bg=colors["card"],
            fg=colors["text"],
        )
        title.grid(row=0, column=0, pady=(0, 6))

        helper = tk.Label(
            inner,
            text="Tick the criteria you want to score on the next screen. You can save this as a template.",
            font=("Segoe UI", 11),
            bg=colors["card"],
            fg=colors["muted"],
            wraplength=680,
            justify="center",
        )
        helper.grid(row=1, column=0, pady=(0, 16))

        checklist_holder = tk.Frame(inner, bg=colors["card"])
        checklist_holder.grid(row=2, column=0, pady=(0, 18), sticky="nsew")

        self.checklist_canvas = tk.Canvas(
            checklist_holder,
            bg=colors["card"],
            highlightthickness=0,
            bd=0,
            height=260,
        )
        self.checklist_canvas.pack(side="left", fill="both", expand=True)

        checklist_scrollbar = ttk.Scrollbar(
            checklist_holder,
            orient="vertical",
            command=self.checklist_canvas.yview
        )
        checklist_scrollbar.pack(side="right", fill="y")

        self.checklist_canvas.configure(yscrollcommand=checklist_scrollbar.set)

        self.checklist_container = tk.Frame(self.checklist_canvas, bg=colors["card"])
        self.checklist_window = self.checklist_canvas.create_window(
            (0, 0),
            window=self.checklist_container,
            anchor="nw"
        )

        self.checklist_container.bind(
            "<Configure>",
            lambda e: self.checklist_canvas.configure(
                scrollregion=self.checklist_canvas.bbox("all")
            )
        )

        self.checklist_canvas.bind("<Configure>", self._resize_checklist_window)
        self.controller.bind_mousewheel(self.checklist_canvas)

        self.rebuild_criteria_list()

        actions = tk.Frame(inner, bg=colors["card"])
        actions.grid(row=3, column=0, pady=(0, 18))

        ttk.Button(
            actions,
            text="Select All",
            style="Dark.TButton",
            command=self.select_all
        ).grid(row=0, column=0, padx=8)

        ttk.Button(
            actions,
            text="Clear All",
            style="Dark.TButton",
            command=self.clear_all
        ).grid(row=0, column=1, padx=8)

        ttk.Button(
            actions,
            text="Add Custom Criterion",
            style="Dark.TButton",
            command=self.open_add_criterion_window
        ).grid(row=0, column=2, padx=8)

        nav = tk.Frame(inner, bg=colors["card"])
        nav.grid(row=4, column=0)

        back_btn = ttk.Button(
            nav,
            text="Back",
            style="Dark.TButton",
            command=lambda: controller.show_frame("SetupSelectionPage")
        )
        back_btn.grid(row=0, column=0, padx=10)

        continue_btn = ttk.Button(
            nav,
            text="Continue",
            style="Accent.TButton",
            command=self.continue_to_main
        )
        continue_btn.grid(row=0, column=1, padx=10)

    def _resize_checklist_window(self, event):
        self.checklist_canvas.itemconfigure(self.checklist_window, width=event.width)

    def rebuild_criteria_list(self):
        for child in self.checklist_container.winfo_children():
            child.destroy()

        all_criteria = self.available_criteria + self.controller.custom_criteria
        cols = 2

        for i, name in enumerate(all_criteria):
            var = self.criteria_vars.get(name)
            if var is None:
                var = tk.BooleanVar(value=False)
                self.criteria_vars[name] = var

            cb = tk.Checkbutton(
                self.checklist_container,
                text=name,
                variable=var,
                bg=self.colors["card"],
                fg=self.colors["text"],
                selectcolor=self.colors["panel"],
                activebackground=self.colors["card"],
                activeforeground=self.colors["text"],
                font=("Segoe UI", 11),
                anchor="w",
                width=30,
            )
            cb.grid(row=i // cols, column=i % cols, sticky="w", padx=10, pady=6)

        self.checklist_canvas.update_idletasks()
        self.checklist_canvas.configure(scrollregion=self.checklist_canvas.bbox("all"))

    def open_add_criterion_window(self):
        popup = tk.Toplevel(self)
        popup.title("Add Custom Criterion")
        popup.geometry("360x170")
        popup.resizable(False, False)
        popup.configure(bg=self.colors["bg"])
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        tk.Label(
            popup,
            text="Enter a name for the new criterion",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["bg"],
            fg="#111827",
        ).pack(pady=(20, 10))

        entry = tk.Entry(
            popup,
            font=("Segoe UI", 11),
            width=30
        )
        entry.pack(pady=(0, 16))
        entry.focus_set()

        btn_row = tk.Frame(popup, bg=self.colors["bg"])
        btn_row.pack()

        def save():
            name = entry.get().strip()

            if not name:
                messagebox.showwarning(
                    "Criterion name required",
                    "Please enter a name for the custom criterion.",
                    parent=popup
                )
                return

            saved = self.controller.add_custom_criterion(name)

            if not saved:
                messagebox.showwarning(
                    "Duplicate criterion",
                    "That criterion already exists.",
                    parent=popup
                )
                return

            self.rebuild_criteria_list()
            popup.destroy()

        ttk.Button(
            btn_row,
            text="Save",
            style="Accent.TButton",
            command=save
        ).grid(row=0, column=0, padx=8)

        ttk.Button(
            btn_row,
            text="Cancel",
            style="Dark.TButton",
            command=popup.destroy
        ).grid(row=0, column=1, padx=8)

        popup.bind("<Return>", lambda event: save())

    def select_all(self):
        for var in self.criteria_vars.values():
            var.set(True)

    def clear_all(self):
        for var in self.criteria_vars.values():
            var.set(False)

    def continue_to_main(self):
        selected = [name for name, var in self.criteria_vars.items() if var.get()]

        if len(selected) < 1:
            messagebox.showwarning(
                "No criteria selected",
                "Please select at least one criterion to continue."
            )
            return

        self.controller.config_state["selected_criteria"] = selected

        if self.controller.template_mode == "create":
            name = simpledialog.askstring(
                "Save Template",
                "Template name (e.g., Maths 1):",
                parent=self
            )
            if name is None:
                return

            name = name.strip()
            if not name:
                messagebox.showwarning(
                    "Template name required",
                    "Please enter a template name."
                )
                return

            saved = self.controller.add_template(name, selected)
            if not saved:
                return

            self.controller.config_state["selected_template_name"] = name
            self.controller.template_mode = None

        self.controller.show_frame("MainPage")

    def refresh(self):
        self.rebuild_criteria_list()
