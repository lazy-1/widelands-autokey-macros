# widelands/core.py
# Minimal entry point: loads tribe + dispatches shortcuts

import os
import sys
import importlib

from .sharedic import USR     # shared dictionary (your global setup)
# No other imports here unless core.py itself calls them directly


# ────────────────────────────────────────────────
# Tribe loading
# ────────────────────────────────────────────────

def import_tribe():
    from .load_config import get_tribe
    get_tribe()

    tribe = USR.get('tribe')
    if not tribe:
        print("ERROR: Tribe not detected after get_tribe()!", file=sys.stderr)
        return

    tribe = tribe.lower().strip()
    tribe_module_name = f"widelands.tribes.{tribe}"

    try:
        mod = importlib.import_module(tribe_module_name)
        
        # Copy public callables into globals (this worked for F1)
        count = 0
        for name in dir(mod):
            if not name.startswith('__'):
                obj = getattr(mod, name)
                if callable(obj):
                    globals()[name] = obj
                    count += 1
        print(f"Loaded tribe '{tribe}' → {count} functions copied (F1 should be there)")
    except ImportError as e:
        print(f"Failed to load '{tribe_module_name}': {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error loading tribe: {e}", file=sys.stderr)

import_tribe()

def call_shortcut(key, keyboard):
    """Main entry point called by AutoKey."""
    USR['keyboard'] = keyboard
    func_name = str(key)  # "F1", "end", "+" etc.

    func = globals().get(func_name)
    if func and callable(func):
        func()
    else:
        print(f"Missing function '{func_name}' for tribe {USR.get('tribe', 'unknown')}")
        # Sound / notification can be added later — keep core clean for now
