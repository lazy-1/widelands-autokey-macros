#!/usr/bin/python3
# config_editor.py
# Standalone Tkinter GUI to edit main settings in user_conf.conf
# Place inside widelands_autokey package

import os
import sys
import configparser
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
    
from tribe_map import _MAPPING

CONFIG_PATH = Path.home() / ".config" / "widelands_autokey" / "user_conf.conf"


def read_config(path: Path) -> configparser.ConfigParser:
    """Load and return configparser object from file.
    Returns empty ConfigParser if file missing or invalid."""
    cfg = configparser.ConfigParser(allow_no_value=True)
    if path.is_file():
        try:
            cfg.read(path)
        except Exception:
            # silent fail → caller handles message
            pass
    return cfg

def write_config(cfg: configparser.ConfigParser, path: Path) -> bool:
    """Write configparser object back to file with a timestamped comment header.
    Returns True on success, False on failure."""

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = [
            f"# Last edited: {timestamp}",
            "# ",
            "# This config file is Produced by ...",
            "# ",
            "# Hand editing is Not recommended",
            "# See .config_template/README-user_conf.txt in the autokey package",
            ""   # empty line after the block
        ]

        with open(path, "w", encoding="utf-8") as f:
            # Write the comment block first
            f.write("\n".join(header) + "\n")
            # Then write the actual config content
            cfg.write(f)

        return True
    except Exception:
        return False

class ConfigEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Widelands Macro Config Editor")
        self.geometry("620x580")
        self.resizable(True, True)
        self.attributes('-topmost', True)
        self.attributes('-type', 'dialog')
        self.cfg = None
        self.entries = {}
        self.checks = {}
        self.race_combo = None

        self.create_widgets()
        self.load_and_populate()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Paths & Flags
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Paths & Flags")

        row = 0

        # Race selection (dropdown)
        ttk.Label(tab1, text="Race / Tribe", font=("Helvetica", 12, "bold")).grid(
            row=row, column=0, sticky="w", pady=(10, 5)
        )
        row += 1

        ttk.Label(tab1, text="Select tribe:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
        self.race_combo = ttk.Combobox(
            tab1,
            values=list(_MAPPING.values()),
            state="readonly",
            width=20,
        )
        self.race_combo.grid(row=row, column=1, sticky="w", padx=5, pady=3)
        row += 2

        # Paths with Browse buttons
        ttk.Label(tab1, text="Paths", font=("Helvetica", 12, "bold")).grid(
            row=row, column=0, sticky="w", pady=(10, 5)
        )
        row += 1

        paths = [
            ("work_path", "[main] work_path","RAM based is better as Road build writes constantly\nwhich is bad for ssd."),
            ("sound_dir", "[main] sound_dir","Your Personal Notifications or where you stored the\nNotifications from the download."),
        ]

        for key, label_text,header_text in paths:

            ttk.Label(tab1, text=header_text).grid(
                row=row, column=1, sticky="w", padx=5, pady=3
            )
            row += 1

            
            ttk.Label(tab1, text=label_text + ":").grid(
                row=row, column=0, sticky="e", padx=5, pady=3
            )

            # Entry field
            e = ttk.Entry(tab1, width=55)
            e.grid(row=row, column=1, sticky="ew", padx=(5, 0), pady=3)

            # Browse button
            btn = ttk.Button(
                tab1,
                text="Browse...",
                width=10,
                command=lambda k=key: self.browse_directory(k)
            )
            btn.grid(row=row, column=2, padx=5, pady=3, sticky="e")

            self.entries[key] = e
            row += 1

        # Booleans
        row += 1
        ttk.Label(tab1, text="Flags", font=("Helvetica", 12, "bold")).grid(
            row=row, column=0, sticky="w", pady=(15, 5)
        )
        row += 1

        flags = [
            ("enable_sounds", "[main] enable_sounds"),
            ("enable_pause", "[main] enable_pause"),
            ("debug", "[main] debug"),
            ("log_enabled", "[main] log_enabled"),
        ]

        for key, label_text in flags:
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(tab1, text=label_text, variable=var)
            cb.grid(row=row, column=0, columnspan=2, sticky="w", padx=5, pady=2)
            self.checks[key] = var
            row += 1

        # Tab 2: Timings & Waits
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Timings & Waits")

        row = 0

        ttk.Label(tab2, text="Timings", font=("Helvetica", 12, "bold")).grid(
            row=row, column=0, sticky="w", pady=(10, 5)
        )
        row += 1

        timings = [
            "delay_stable_settle",
            "delay_click_hold",
            "warp_settle",
            "click_hold",
            "ctrl_press_delay",
        ]

        for key in timings:
            ttk.Label(tab2, text=f"{key}:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
            e = ttk.Entry(tab2, width=12)
            e.grid(row=row, column=1, sticky="w", padx=5, pady=3)
            self.entries[key] = e
            row += 1

        row += 1
        ttk.Label(tab2, text="Waits", font=("Helvetica", 12, "bold")).grid(
            row=row, column=0, sticky="w", pady=(15, 5)
        )
        row += 1

        waits = [
            "wait_for_dialog1",
            "wait1",
            "wait_for_dialog2",
            "wait_to_register1",
            "wait_for_dialog3",
            "wait_to_register2",
            "wait_screenshot",
            "wait_to_register3",
        ]

        for key in waits:
            ttk.Label(tab2, text=f"{key}:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
            e = ttk.Entry(tab2, width=12)
            e.grid(row=row, column=1, sticky="w", padx=5, pady=3)
            self.entries[key] = e
            row += 1

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=15)

        ttk.Button(btn_frame, text="Save", command=self.save).pack(side="right", padx=20)
        ttk.Button(btn_frame, text="Reload", command=self.load_and_populate).pack(
            side="right", padx=10
        )
        ttk.Button(btn_frame, text="Quit", command=self.destroy).pack(side="right")

        tab1.columnconfigure(1, weight=1)
        tab2.columnconfigure(1, weight=1)

    def browse_directory(self, key):
        """Open directory browser, allow selection or creation, update entry."""
        initial_dir = self.entries[key].get().strip() or str(Path.home())
        if not os.path.isdir(initial_dir):
            initial_dir = str(Path.home())

        chosen_dir = filedialog.askdirectory(
            title=f"Select or create directory for {key}",
            initialdir=initial_dir,
            mustexist=False
        )

        if not chosen_dir:
            return

        chosen_dir = chosen_dir.strip()

        if key == "sound_dir":
            chosen_dir = os.path.join(chosen_dir, "")

        if not os.path.isdir(chosen_dir):
            if messagebox.askyesno(
                "Create directory?",
                f"The folder\n{chosen_dir}\ndoes not exist.\n\nCreate it now?"
            ):
                try:
                    os.makedirs(chosen_dir, exist_ok=True)
                    messagebox.showinfo("Created", f"Directory created:\n{chosen_dir}")
                except Exception as e:
                    messagebox.showerror("Creation failed", f"Could not create folder:\n{e}")
                    return
            else:
                return

        self.entries[key].delete(0, tk.END)
        self.entries[key].insert(0, chosen_dir)

    def load_and_populate(self):
        """(Re)load config and fill GUI fields"""
        self.cfg = read_config(CONFIG_PATH)

        if not self.cfg.sections():
            messagebox.showerror("Error", f"Could not load config:\n{CONFIG_PATH}")
            return

        # Race / Tribe dropdown
        race_num = self.cfg.getint("main", "race_number", fallback=0)
        tribe_name = _MAPPING.get(race_num, "Amazon")
        self.race_combo.set(tribe_name)

        # Paths
        for key in ["work_path", "sound_dir"]:
            if key in self.entries:
                val = self.cfg.get("main", key, fallback="")
                entry = self.entries[key]
                entry.configure(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, val)

        # Booleans
        for key, var in self.checks.items():
            val = self.cfg.get("main", key, fallback="false").lower()
            var.set(val in ("true", "yes", "1", "on"))

        # Float fields (timings & waits)
        float_keys = set(self.entries) - {"work_path", "sound_dir"}
        for key in float_keys:
            val = self.cfg.get(
                "timings" if "delay_" in key or "settle" in key or "hold" in key else "waits",
                key,
                fallback="0.05",
            )
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, val)

    def save(self):
        """Collect GUI values → update config → write file"""
        if not self.cfg:
            messagebox.showerror("Error", "No config loaded")
            return

        try:
            # Race
            selected_tribe = self.race_combo.get()
            race_num = next(
                (k for k, v in _MAPPING.items() if v == selected_tribe), 0
            )
            self.cfg["main"]["race_number"] = str(race_num)

            # Paths
            for key in ["work_path", "sound_dir"]:
                if key in self.entries:
                    self.cfg["main"][key] = self.entries[key].get().strip()

            # Booleans
            for key, var in self.checks.items():
                self.cfg["main"][key] = "true" if var.get() else "false"

            # Floats (timings)
            for key in [
                "delay_stable_settle",
                "delay_click_hold",
                "warp_settle",
                "click_hold",
                "ctrl_press_delay",
            ]:
                try:
                    float(self.entries[key].get())
                    self.cfg["timings"][key] = self.entries[key].get().strip()
                except ValueError:
                    messagebox.showwarning("Invalid", f"{key} must be a number")
                    return

            # Floats (waits)
            for key in [
                "wait_for_dialog1",
                "wait1",
                "wait_for_dialog2",
                "wait_to_register1",
                "wait_for_dialog3",
                "wait_to_register2",
                "wait_screenshot",
                "wait_to_register3",
            ]:
                try:
                    float(self.entries[key].get())
                    self.cfg["waits"][key] = self.entries[key].get().strip()
                except ValueError:
                    messagebox.showwarning("Invalid", f"{key} must be a number")
                    return

            if write_config(self.cfg, CONFIG_PATH):
                messagebox.showinfo("Saved", "Changes saved.")
            else:
                messagebox.showerror("Save failed", "Could not write file.")

        except Exception as e:
            messagebox.showerror("Save error", str(e))

if __name__ == "__main__":
    app = ConfigEditor()
    app.mainloop()
