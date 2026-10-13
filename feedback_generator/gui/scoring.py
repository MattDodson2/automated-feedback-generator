"""MainPage GUI view (extracted from the original Tkinter application)."""

import tkinter as tk
from tkinter import ttk, messagebox


class MainPage(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors["bg"])
        self.controller = controller
        self.colors = colors
        self.criteria_rows = []

        header = tk.Frame(self, bg=colors["panel"], height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Score Input",
            font=("Segoe UI", 16, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        ).pack(side="left", padx=20, pady=18)

        outer = tk.Frame(self, bg=colors["bg"])
        outer.pack(fill="both", expand=True, padx=30, pady=18)

        outer.grid_columnconfigure(0, weight=1)
        outer.grid_columnconfigure(1, weight=1)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_rowconfigure(1, weight=1)

        left_card = tk.Frame(outer, bg=colors["panel"], width=480, height=430)
        left_card.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10), pady=(0, 14))
        left_card.grid_propagate(False)

        left_accent = tk.Frame(left_card, bg=colors["accent"], height=6)
        left_accent.pack(fill="x", side="top")

        tk.Label(
            left_card,
            text="Input Criteria Score",
            font=("Segoe UI", 16, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        ).pack(pady=(40, 12))

        tk.Label(
            left_card,
            text="Select a value 1–5 based on how strong\nyou think this area was",
            font=("Segoe UI", 9, "bold"),
            bg=colors["panel"],
            fg=colors["muted"],
            justify="center",
        ).pack()

        criteria_area = tk.Frame(left_card, bg=colors["panel"])
        criteria_area.pack(fill="both", expand=True, padx=18, pady=(24, 18))

        self.criteria_canvas = tk.Canvas(
            criteria_area,
            bg=colors["panel"],
            highlightthickness=0,
            bd=0,
        )
        self.criteria_canvas.pack(side="left", fill="both", expand=True)

        criteria_scrollbar = ttk.Scrollbar(
            criteria_area,
            orient="vertical",
            command=self.criteria_canvas.yview
        )
        criteria_scrollbar.pack(side="right", fill="y")

        self.criteria_canvas.configure(yscrollcommand=criteria_scrollbar.set)

        self.criteria_container = tk.Frame(self.criteria_canvas, bg=colors["panel"])
        self.criteria_window = self.criteria_canvas.create_window(
            (0, 0),
            window=self.criteria_container,
            anchor="n"
        )

        self.criteria_container.bind(
            "<Configure>",
            lambda e: self.criteria_canvas.configure(scrollregion=self.criteria_canvas.bbox("all"))
        )

        self.criteria_canvas.bind("<Configure>", self._resize_criteria_window)
        self.controller.bind_mousewheel(self.criteria_canvas)

        grade_card = tk.Frame(outer, bg=colors["panel"], width=395, height=175)
        grade_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 14))
        grade_card.grid_propagate(False)

        grade_accent = tk.Frame(grade_card, bg=colors["accent"], height=6)
        grade_accent.pack(fill="x", side="top")

        tk.Label(
            grade_card,
            text="Grade",
            font=("Segoe UI", 15, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        ).pack(pady=(38, 14))

        scale_row = tk.Frame(grade_card, bg=colors["panel"])
        scale_row.pack()

        tk.Label(
            scale_row,
            text="0",
            font=("Segoe UI", 11, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        ).pack(side="left", padx=(0, 12))

        self.grade_scale = tk.Scale(
            scale_row,
            from_=0,
            to=100,
            orient="horizontal",
            resolution=10,
            length=310,
            showvalue=False,
            bg=colors["accent"],
            fg=colors["text"],
            highlightthickness=0,
            bd=0,
            troughcolor="white",
            activebackground=colors["accent"],
            command=self.update_grade_label,
        )
        self.grade_scale.set(40)
        self.grade_scale.pack(side="left")

        tk.Label(
            scale_row,
            text="100",
            font=("Segoe UI", 11, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        ).pack(side="left", padx=(12, 0))

        self.grade_value_label = tk.Label(
            grade_card,
            text="40",
            font=("Segoe UI", 11, "bold"),
            bg=colors["accent"],
            fg="white",
            width=4,
            pady=8,
        )
        self.grade_value_label.pack(pady=(18, 0))

        info_card = tk.Frame(outer, bg=colors["panel"], width=395, height=240)
        info_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        info_card.grid_propagate(False)

        info_accent = tk.Frame(info_card, bg=colors["accent"], height=6)
        info_accent.pack(fill="x", side="top")

        info_text = (
            "Select a score from 1 to 5 for each of your selected criteria\n\n"
            "Enter an optional comment next to any area you think might need a more detailed\n"
            "description\n\n"
            "Use the slider in the box above to select the grade boundary your student achieved\n\n"
            "Once you're done, go ahead and click the “Generate Feedback” button below to receive\n"
            "your automated feedback"
        )

        tk.Label(
            info_card,
            text=info_text,
            font=("Segoe UI", 8, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
            justify="center",
            wraplength=320,
        ).pack(expand=True)

        bottom = tk.Frame(self, bg=colors["bg"])
        bottom.pack(fill="x", padx=42, pady=(0, 16))

        ttk.Button(
            bottom,
            text="Back",
            style="Dark.TButton",
            command=lambda: controller.show_frame("SetupSelectionPage")
        ).pack(side="left")

        ttk.Button(
            bottom,
            text="Generate Feedback",
            style="Accent.TButton",
            command=self.go_to_output
        ).pack(side="right")

    def _resize_criteria_window(self, event):
        self.criteria_canvas.itemconfigure(self.criteria_window, width=event.width)

    def build_criteria_rows(self):
        for child in self.criteria_container.winfo_children():
            child.destroy()

        self.criteria_rows.clear()

        selected = self.controller.config_state.get("selected_criteria", [])

        if not selected:
            tk.Label(
                self.criteria_container,
                text="No criteria selected.",
                font=("Segoe UI", 12),
                bg=self.colors["panel"],
                fg=self.colors["text"],
            ).pack()
            return

        for index, criterion in enumerate(selected):
            row_frame = tk.Frame(self.criteria_container, bg=self.colors["panel"])
            row_frame.grid(row=index, column=0, pady=10, padx=20, sticky="w")

            tk.Label(
                row_frame,
                text=criterion,
                font=("Segoe UI", 11, "bold"),
                bg=self.colors["panel"],
                fg=self.colors["text"],
                width=18,
                anchor="e",
            ).pack(side="left", padx=(0, 8))

            score_var = tk.StringVar(value="1")
            score_box = ttk.Combobox(
                row_frame,
                textvariable=score_var,
                values=["1", "2", "3", "4", "5"],
                width=3,
                state="readonly",
            )
            score_box.pack(side="left", padx=(0, 10))

            if criterion == "Analysis":
                comment_box = tk.Entry(
                    row_frame,
                    width=28,
                    font=("Segoe UI", 10),
                )
                comment_box.insert(0, "")
                comment_box.pack(side="left")

                self.criteria_rows.append({
                    "criterion": criterion,
                    "score_var": score_var,
                    "comment_widget": comment_box,
                })
            else:
                self.criteria_rows.append({
                    "criterion": criterion,
                    "score_var": score_var
                })

        self.criteria_canvas.yview_moveto(0)

    def update_grade_label(self, value):
        self.grade_value_label.config(text=str(int(float(value))))

    def go_to_output(self):
        collected = []
        for row in self.criteria_rows:
            comment = row["comment_widget"].get().strip() if "comment_widget" in row else ""
            collected.append({
                "criterion": row["criterion"],
                "score": int(row["score_var"].get()),
                "comment": comment,
            })

        grade = self.grade_scale.get()

        self.controller.config_state["criteria_inputs"] = collected
        self.controller.config_state["grade"] = grade

        try:
            results = self.controller.feedback_engine.generate_multiple_feedback(
                collected,
                grade,
                count=3
            )

            if not results:
                raise ValueError("No feedback versions could be generated.")

            self.controller.config_state["generated_versions"] = results
            self.controller.config_state["current_version_index"] = 0
            self.controller.config_state["generated_feedback"] = results[0]
            self.controller.show_frame("OutputPage")

        except Exception as exc:
            messagebox.showerror(
                "Feedback generation error",
                f"The feedback could not be generated.\n\n{exc}"
            )

    def refresh(self):
        self.build_criteria_rows()
        self.grade_scale.set(40)
        self.grade_value_label.config(text="40")
