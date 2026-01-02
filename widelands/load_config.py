# load_config.py
# ────────────────────────────────────────────────────────────────
# This file handles:
#   - Tribe mapping and selection (get_tribe())
#   - Auto-creation and loading of the user config file
#
# It does NOTHING else — no USR population except 'tribe'.
# All other USR values are loaded elsewhere or left to defaults.
# ────────────────────────────────────────────────────────────────

import os
import shutil
import importlib.util
import sys
from pathlib import Path

from .sharedic import USR

# ────────────────────────────────────────────────────────────────
# Tribe mapping — used by get_tribe()
# ────────────────────────────────────────────────────────────────
_MAPPING = {
    0: 'Amazon',
    1: 'Atlantean',
    2: 'Barbarian',
    3: 'Empire',
    4: 'Frisian',
}


def get_tribe():
    global USR
    load_USR_defaults()
    num = USR.get('race_number', 0)  # defaults to 0 if missing
    tribe = _MAPPING.get(num, 'Amazon')  # safe fallback
    USR['tribe'] = tribe
    return tribe


def load_USR_defaults():
    """
    Creates user config, updates USR.
    """

    config_dir = Path.home() / '.config' / 'widelands_autokey'
    config_file = config_dir / 'user_config.py'

    config_dir.mkdir(parents=True, exist_ok=True)

    template_file = Path(__file__).parent / '.config_template' / 'user_config.py'

    # Copy template if user config missing
    if not config_file.exists():
        if template_file.exists():
            shutil.copy(template_file, config_file)
            print(f"Created user config: {config_file}")
        else:
            print(f"Template missing: {template_file}")
            print("Cannot continue — exiting.")
            sys.exit(1)

    # Load user config dynamically
    spec = importlib.util.spec_from_file_location("user_config", config_file)
    if spec is None:
        print(f"Failed to load user config: {config_file}")
        sys.exit(1)

    user_config = importlib.util.module_from_spec(spec)
    sys.modules["user_config"] = user_config

    try:
        spec.loader.exec_module(user_config)
        settings_dict = user_config.load_the_config()
        USR.update(settings_dict)
    except Exception as e:
        print(f"ERROR: user_config.py is corrupt or invalid: {e}")
        print("Fallback: Manually copy template to overwrite your config file.")
        print(f"Template location: {template_file}")
        print(f"Target location: {config_file}")
        print("1. Copy the template file to the target location")
        print("2. Edit the copied file with your settings")
        print("3. Reload AutoKey")
        sys.exit(1)  # or continue with defaults if you prefer not to exit

