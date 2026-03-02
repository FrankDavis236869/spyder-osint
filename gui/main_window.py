#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Tkinter window for Spyder OSINT
"""

import subprocess
import sys
import threading
from pathlib import Path

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional

from core.processor import Processor
from utils.file_handler import FileHandler
from utils.logger import get_logger

logger = get_logger(__name__)

QUERY_TYPES = [
    ("phone", "Phone number"),
    ("ip", "IP address"),
    ("email", "Email"),
    ("domain", "Domain"),
    ("username", "Username"),
    ("name", "Person's name"),
    ("address", "Physical address"),
    ("plate", "License plate (EU/Asia)"),
]


class MainWindow:
    """Main application window."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spyder OSINT - Research Tool")
        self.root.geometry("700x550")
        self.root.minsize(500, 400)

        self.processor = Processor()
        self.file_handler = FileHandler()

        self._build_ui()

    def _build_ui(self):
        # Header
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill=tk.X)
        ttk.Label(header, text="Spyder OSINT", font=("Segoe UI", 18, "bold")).pack()
        ttk.Label(header, text="Universal open-source intelligence research", font=("Segoe UI", 10)).pack()

        # Input section
        input_frame = ttk.LabelFrame(self.root, text="Query", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(input_frame, text="Input:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry = ttk.Entry(input_frame, width=50)
        self.entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)
        self.entry.bind("<Return>", lambda e: self._on_search())

        ttk.Label(input_frame, text="Type:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.type_var = tk.StringVar(value="IP address")
        type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, width=47, state="readonly")
        type_combo["values"] = [t[1] for t in QUERY_TYPES]
        type_combo.grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)
        self._type_map = {t[1]: t[0] for t in QUERY_TYPES}

        input_frame.columnconfigure(1, weight=1)

        # Buttons
        btn_frame = ttk.Frame(self.root, padding=5)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="[1] Install dependencies", command=self._on_install_deps).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="[2] Search", command=self._on_search).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="[3] Clear", command=self._on_clear).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="[4] Export", command=self._on_export).pack(side=tk.LEFT, padx=2)

        def _key(handler):
            def _h(e):
                w = self.root.focus_get()
                if w in (self.entry, self.output):
                    return
                handler()
            return _h

        for key, handler in [("1", self._on_install_deps), ("2", self._on_search),
                            ("3", self._on_clear), ("4", self._on_export)]:
            self.root.bind(f"<KeyPress-{key}>", _key(handler))

        # Results
        result_frame = ttk.LabelFrame(self.root, text="Results", padding=5)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.output = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=15, font=("Consolas", 10))
        self.output.pack(fill=tk.BOTH, expand=True)
        self._results: list = []

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def _on_search(self):
        query = self.entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Enter a query.")
            return

        type_display = self.type_var.get()
        query_type = self._type_map.get(type_display, "username")

        self.output.insert(tk.END, f"\n>>> Query: {query} (type: {query_type})\n", "query")
        self.root.update_idletasks()

        try:
            result = self.processor.process(query, query_type)
            text = self._format_result(result)
            self.output.insert(tk.END, text + "\n", "result")
            self._results.append(result)
        except Exception as e:
            logger.exception("Search failed")
            self.output.insert(tk.END, f"Error: {e}\n", "error")
            messagebox.showerror("Error", str(e))

        self.output.see(tk.END)

    def _format_result(self, result: dict) -> str:
        lines = []
        for k, v in result.items():
            if k.startswith("_"):
                continue
            if isinstance(v, dict):
                lines.append(f"  {k}:")
                for k2, v2 in v.items():
                    lines.append(f"    {k2}: {v2}")
            else:
                lines.append(f"  {k}: {v}")
        return "\n".join(lines) if lines else str(result)

    def _on_clear(self):
        self.output.delete(1.0, tk.END)
        self._results.clear()
        self.entry.delete(0, tk.END)

    def _on_export(self):
        if not self._results:
            messagebox.showinfo("Info", "No results to export.")
            return
        path = self.file_handler.export_results(self._results)
        messagebox.showinfo("Exported", f"Saved to:\n{path}")

    def _on_install_deps(self):
        """Run pip install -r requirements.txt in background."""
        req_path = Path(__file__).resolve().parent.parent / "requirements.txt"
        if not req_path.exists():
            messagebox.showerror("Error", f"requirements.txt not found:\n{req_path}")
            return

        def run_install():
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(req_path)],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                output = (result.stdout or "") + (result.stderr or "")
                self.root.after(0, lambda: self._show_install_result(result.returncode == 0, output))
            except subprocess.TimeoutExpired:
                self.root.after(0, lambda: self._show_install_result(False, "Installation timeout."))
            except Exception as e:
                self.root.after(0, lambda: self._show_install_result(False, str(e)))

        threading.Thread(target=run_install, daemon=True).start()
        messagebox.showinfo("Installing", "Dependencies are being installed in the background.\n"
                            "A message will appear when complete.")

    def _show_install_result(self, success: bool, output: str):
        if success:
            messagebox.showinfo("Done", "Dependencies installed successfully.")
        else:
            messagebox.showerror("Install failed", f"pip install failed:\n\n{output[:500]}")

    def run(self):
        self.output.tag_configure("query", foreground="blue")
        self.output.tag_configure("result", foreground="black")
        self.output.tag_configure("error", foreground="red")
        self.root.mainloop()
