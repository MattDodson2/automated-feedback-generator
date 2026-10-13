"""OutputPage GUI view (extracted from the original Tkinter application)."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class OutputPage(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors["bg"])
        self.controller = controller
        self.colors = colors

        header = tk.Frame(self, bg=colors["panel"], height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Feedback Output",
            font=("Segoe UI", 16, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        ).pack(side="left", padx=20, pady=18)

        outer = tk.Frame(self, bg=colors["bg"])
        outer.pack(fill="both", expand=True, padx=28, pady=14)

        outer.grid_columnconfigure(0, weight=4)
        outer.grid_columnconfigure(1, weight=0)
        outer.grid_columnconfigure(2, weight=2)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_rowconfigure(1, weight=0)

        left_card = tk.Frame(outer, bg=colors["panel"])
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 18))

        left_accent = tk.Frame(left_card, bg=colors["accent"], height=6)
        left_accent.pack(fill="x", side="top")

        left_inner = tk.Frame(left_card, bg=colors["panel"])
        left_inner.pack(fill="both", expand=True, padx=12, pady=12)

        left_inner.grid_columnconfigure(0, weight=1)
        left_inner.grid_rowconfigure(3, weight=1)

        tk.Label(
            left_inner,
            text="Generated Feedback",
            font=("Segoe UI", 15, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        ).grid(row=0, column=0, pady=(6, 10))

        intro_text = (
            "Here’s what I came up with based your inputs. If you’d like to change any of my feedback, feel free to\n"
            "edit the text in the box below OR click the Regenerate Feedback button and I’ll have another go"
        )

        tk.Label(
            left_inner,
            text=intro_text,
            font=("Segoe UI", 10),
            bg=colors["panel"],
            fg=colors["text"],
            justify="center",
        ).grid(row=1, column=0, pady=(0, 14))

        version_row = tk.Frame(left_inner, bg=colors["panel"])
        version_row.grid(row=2, column=0, pady=(0, 12))

        self.version_label = tk.Label(
            version_row,
            text="Version 1 of 1",
            font=("Segoe UI", 10, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        )
        self.version_label.pack(side="left", padx=(0, 12))

        self.prev_version_btn = tk.Button(
            version_row,
            text="Previous",
            font=("Segoe UI", 9, "bold"),
            bg=colors["accent"],
            fg="white",
            activebackground=colors["accent"],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            command=self.show_previous_version
        )
        self.prev_version_btn.pack(side="left", padx=4)

        self.next_version_btn = tk.Button(
            version_row,
            text="Next",
            font=("Segoe UI", 9, "bold"),
            bg=colors["accent"],
            fg="white",
            activebackground=colors["accent"],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            command=self.show_next_version
        )
        self.next_version_btn.pack(side="left", padx=4)

        text_frame = tk.Frame(left_inner, bg=colors["panel"])
        text_frame.grid(row=3, column=0, sticky="nsew")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        self.feedback_text = tk.Text(
            text_frame,
            wrap="word",
            font=("Segoe UI", 11),
            bg="white",
            fg="#111827",
            relief="flat",
            bd=0,
            padx=12,
            pady=12,
            insertbackground="#111827",
        )
        self.feedback_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.feedback_text.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.feedback_text.configure(yscrollcommand=scrollbar.set)

        right_col = tk.Frame(outer, bg=colors["bg"])
        right_col.grid(row=0, column=2, sticky="nsew")

        right_col.grid_columnconfigure(0, weight=1)
        right_col.grid_rowconfigure(2, weight=1)

        info_card = tk.Frame(right_col, bg=colors["panel"], width=260, height=95)
        info_card.grid(row=0, column=0, sticky="ew", pady=(0, 26))
        info_card.grid_propagate(False)

        info_accent = tk.Frame(info_card, bg=colors["accent"], height=6)
        info_accent.pack(fill="x", side="top")

        info_inner = tk.Frame(info_card, bg=colors["panel"])
        info_inner.pack(fill="both", expand=True, padx=12, pady=12)

        self.grade_label = tk.Label(
            info_inner,
            text="Grade: --",
            font=("Segoe UI", 11),
            bg=colors["panel"],
            fg=colors["text"],
            anchor="w",
        )
        self.grade_label.pack(fill="x", pady=(0, 12))

        self.template_label = tk.Label(
            info_inner,
            text="Template used: --",
            font=("Segoe UI", 11),
            bg=colors["panel"],
            fg=colors["text"],
            anchor="w",
        )
        self.template_label.pack(fill="x")

        regen_holder = tk.Frame(right_col, bg=colors["bg"])
        regen_holder.grid(row=1, column=0, sticky="ew", pady=(0, 18))

        tk.Button(
            regen_holder,
            text="Regenerate Feedback",
            font=("Segoe UI", 10, "bold"),
            bg=colors["accent"],
            fg="white",
            activebackground=colors["accent"],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            command=self.regenerate_feedback
        ).pack()

        actions_card = tk.Frame(right_col, bg=colors["panel"])
        actions_card.grid(row=2, column=0, sticky="nsew")

        actions_accent = tk.Frame(actions_card, bg=colors["accent"], height=6)
        actions_accent.pack(fill="x", side="top")

        actions_inner = tk.Frame(actions_card, bg=colors["panel"])
        actions_inner.pack(fill="both", expand=True, padx=16, pady=28)

        tk.Button(
            actions_inner,
            text="Copy to Clipboard",
            font=("Segoe UI", 9, "bold"),
            bg=colors["accent"],
            fg="white",
            activebackground=colors["accent"],
            activeforeground="white",
            relief="flat",
            bd=0,
            width=18,
            pady=10,
            command=self.copy_to_clipboard
        ).pack(pady=(0, 20))

        tk.Button(
            actions_inner,
            text="Export as Text File",
            font=("Segoe UI", 9, "bold"),
            bg=colors["accent"],
            fg="white",
            activebackground=colors["accent"],
            activeforeground="white",
            relief="flat",
            bd=0,
            width=18,
            pady=10,
            command=self.export_to_file
        ).pack(pady=(0, 20))

        tk.Button(
            actions_inner,
            text="Clear text",
            font=("Segoe UI", 9, "bold"),
            bg=colors["accent"],
            fg="white",
            activebackground=colors["accent"],
            activeforeground="white",
            relief="flat",
            bd=0,
            width=18,
            pady=10,
            command=self.clear_text
        ).pack()

        bottom_bar = tk.Frame(outer, bg=colors["bg"])
        bottom_bar.grid(row=1, column=0, columnspan=3, sticky="w", pady=(14, 0))

        tk.Button(
            bottom_bar,
            text="Back",
            font=("Segoe UI", 10, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
            activebackground=colors["panel"],
            activeforeground=colors["text"],
            relief="flat",
            bd=0,
            width=10,
            pady=8,
            command=lambda: controller.show_frame("MainPage")
        ).pack(side="left")

    def refresh(self):
        versions = self.controller.config_state.get("generated_versions", [])
        current_index = self.controller.config_state.get("current_version_index", 0)
        template_name = self.controller.config_state.get("selected_template_name")

        if not versions:
            self.grade_label.config(text="Grade: --")
            self.template_label.config(
                text=f"Template used: {template_name if template_name else 'None'}"
            )
            self.version_label.config(text="Version 0 of 0")
            self._set_feedback_text("No feedback has been generated yet.")
            self.prev_version_btn.config(state="disabled")
            self.next_version_btn.config(state="disabled")
            return

        current_index = max(0, min(current_index, len(versions) - 1))
        result = versions[current_index]

        self.controller.config_state["generated_feedback"] = result
        self.controller.config_state["current_version_index"] = current_index

        self.grade_label.config(text=f"Grade: {result['grade']}")
        self.template_label.config(
            text=f"Template used: {template_name if template_name else 'None'}"
        )
        self.version_label.config(text=f"Version {current_index + 1} of {len(versions)}")
        self._set_feedback_text(result["final_feedback"])

        if current_index == 0:
            self.prev_version_btn.config(state="disabled")
        else:
            self.prev_version_btn.config(state="normal")

        if current_index == len(versions) - 1:
            self.next_version_btn.config(state="disabled")
        else:
            self.next_version_btn.config(state="normal")

    def _set_feedback_text(self, text):
        self.feedback_text.delete("1.0", "end")
        self.feedback_text.insert("1.0", text)

    def get_current_text(self):
        return self.feedback_text.get("1.0", "end-1c")

    def copy_to_clipboard(self):
        text = self.get_current_text()
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
        messagebox.showinfo("Copied", "Feedback copied to clipboard.")

    def clear_text(self):
        self.feedback_text.delete("1.0", "end")

    def export_to_file(self):
        text = self.get_current_text()
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Feedback As"
        )

        if not filepath:
            return

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Saved", "Feedback exported successfully.")
        except Exception as exc:
            messagebox.showerror("Save error", f"Could not save file.\n\n{exc}")

    def regenerate_feedback(self):
        criteria_inputs = self.controller.config_state.get("criteria_inputs", [])
        grade = self.controller.config_state.get("grade", 0)

        try:
            results = self.controller.feedback_engine.generate_multiple_feedback(
                criteria_inputs,
                grade,
                count=3
            )

            if not results:
                raise ValueError("No feedback versions could be generated.")

            self.controller.config_state["generated_versions"] = results
            self.controller.config_state["current_version_index"] = 0
            self.controller.config_state["generated_feedback"] = results[0]
            self.refresh()

        except Exception as exc:
            messagebox.showerror(
                "Feedback generation error",
                f"The feedback could not be regenerated.\n\n{exc}"
            )

    def show_previous_version(self):
        versions = self.controller.config_state.get("generated_versions", [])
        current_index = self.controller.config_state.get("current_version_index", 0)

        if not versions:
            return

        if current_index > 0:
            current_index -= 1
            self.controller.config_state["current_version_index"] = current_index
            self.controller.config_state["generated_feedback"] = versions[current_index]
            self.refresh()

    def show_next_version(self):
        versions = self.controller.config_state.get("generated_versions", [])
        current_index = self.controller.config_state.get("current_version_index", 0)

        if not versions:
            return

        if current_index < len(versions) - 1:
            current_index += 1
            self.controller.config_state["current_version_index"] = current_index
            self.controller.config_state["generated_feedback"] = versions[current_index]
            self.refresh()
