"""SetupSelectionPage GUI view (extracted from the original Tkinter application)."""

import tkinter as tk
from tkinter import ttk


class SetupSelectionPage(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors["bg"])
        self.controller = controller
        self.colors = colors

        header = tk.Frame(self, bg=colors["panel"], height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        header_title = tk.Label(
            header,
            text="Setup Templates",
            font=("Segoe UI", 16, "bold"),
            bg=colors["panel"],
            fg=colors["text"],
        )
        header_title.pack(side="left", padx=20)

        scroll_container = tk.Frame(self, bg=colors["bg"])
        scroll_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            scroll_container,
            bg=colors["bg"],
            highlightthickness=0
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            scroll_container,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scroll_frame = tk.Frame(self.canvas, bg=colors["bg"])
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.controller.bind_mousewheel(self.canvas)

        self.main = self.scroll_frame

        create_label = tk.Label(
            self.main,
            text="Create New",
            font=("Segoe UI", 14, "bold"),
            bg=colors["bg"],
            fg="#111827",
        )
        create_label.pack(anchor="w", padx=40, pady=(30, 0))

        create_row = tk.Frame(self.main, bg=colors["bg"])
        create_row.pack(fill="x", padx=40, pady=(10, 30))

        plus_btn = tk.Button(
            create_row,
            text="+",
            font=("Segoe UI", 18, "bold"),
            width=4,
            height=2,
            bd=0,
            bg=colors["card"],
            fg=colors["text"],
            activebackground=colors["panel"],
            activeforeground=colors["text"],
            command=self.controller.start_new_template
        )
        plus_btn.pack(anchor="w")

        load_label = tk.Label(
            self.main,
            text="Load Previous",
            font=("Segoe UI", 14, "bold"),
            bg=colors["bg"],
            fg="#111827",
        )
        load_label.pack(anchor="w", padx=40, pady=(0, 10))

        self.tiles = tk.Frame(self.main, bg=colors["bg"])
        self.tiles.pack(fill="both", expand=True, padx=40)

        bottom = tk.Frame(self, bg=colors["bg"])
        bottom.pack(fill="x", pady=10)

        back_btn = ttk.Button(
            bottom,
            text="Back",
            style="Dark.TButton",
            command=lambda: controller.show_frame("HomePage")
        )
        back_btn.pack(anchor="w", padx=40)

    def refresh(self):
        for child in self.tiles.winfo_children():
            child.destroy()

        templates = self.controller.templates

        if not templates:
            empty = tk.Label(
                self.tiles,
                text="No saved templates yet. Click + to create your first one.",
                font=("Segoe UI", 11),
                bg=self.colors["bg"],
                fg="#374151",
            )
            empty.pack(anchor="w", pady=10)
            return

        cols = 4
        for i, t in enumerate(templates):
            tile = tk.Button(
                self.tiles,
                text=t["name"],
                font=("Segoe UI", 12, "bold"),
                width=16,
                height=4,
                bd=0,
                bg=self.colors["card"],
                fg=self.colors["text"],
                activebackground=self.colors["panel"],
                activeforeground=self.colors["text"],
                command=lambda template=t: self.controller.use_template(template),
            )
            tile.grid(row=i // cols, column=i % cols, padx=15, pady=12)
