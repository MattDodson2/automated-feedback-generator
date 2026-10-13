"""HomePage GUI view (extracted from the original Tkinter application)."""

import tkinter as tk
from tkinter import ttk


class HomePage(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors["bg"])
        self.controller = controller
        self.colors = colors

        header = tk.Frame(self, bg=colors["panel"], height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        header_title = tk.Label(
            header,
            text="Welcome",
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
        card.grid(row=0, column=0, padx=40, pady=40)
        card.configure(width=720, height=360)
        card.grid_propagate(False)

        accent = tk.Frame(card, bg=colors["accent"], height=6)
        accent.pack(fill="x", side="top")

        inner = tk.Frame(card, bg=colors["card"])
        inner.pack(fill="both", expand=True, padx=40, pady=28)

        title_label = tk.Label(
            inner,
            text="Automated Feedback Generator",
            font=("Segoe UI", 24, "bold"),
            bg=colors["card"],
            fg=colors["text"],
        )
        title_label.pack(pady=(0, 6))

        subtitle = tk.Label(
            inner,
            text="Generate consistent, editable feedback from your marking criteria",
            font=("Segoe UI", 11),
            bg=colors["card"],
            fg=colors["muted"],
        )
        subtitle.pack(pady=(0, 18))

        description_text = (
            "This app helps you create realistic written feedback for students.\n\n"
            "Save your criteria setups as templates so you can reuse them every time."
        )

        description_label = tk.Label(
            inner,
            text=description_text,
            font=("Segoe UI", 12),
            bg=colors["card"],
            fg=colors["muted"],
            wraplength=600,
            justify="center",
        )
        description_label.pack(pady=(0, 24))

        btn_row = tk.Frame(inner, bg=colors["card"])
        btn_row.pack()

        start_btn = ttk.Button(
            btn_row,
            text="Start",
            style="Accent.TButton",
            command=lambda: controller.show_frame("SetupSelectionPage"),
        )
        start_btn.grid(row=0, column=0, padx=10)

        exit_btn = ttk.Button(
            btn_row,
            text="Exit",
            style="Dark.TButton",
            command=controller.destroy
        )
        exit_btn.grid(row=0, column=1, padx=10)

        bottom_bar = tk.Frame(self, bg=colors["bg"])
        bottom_bar.pack(fill="x", side="bottom", padx=20, pady=14)

        settings_btn = tk.Button(
            bottom_bar,
            text="⚙ Settings",
            font=("Segoe UI", 9),
            bg=colors["bg"],
            fg="#293039",
            activebackground=colors["bg"],
            activeforeground="#111827",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: controller.show_frame("SettingsPage"),
        )
        settings_btn.pack(side="left", anchor="sw")
