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
import sys
from pathlib import Path
import configparser

from .sharedic import USR
from .tribe_map import _MAPPING



def get_tribe():
    global USR
    load_USR_defaults()
    num = USR.get('race_number', 0)  # defaults to 0 if missing
    tribe = _MAPPING.get(num, 'Amazon')  # safe fallback
    USR['tribe'] = tribe
    return tribe


def load_configparser_flat(path: str | Path) -> dict:
    """
    Reusable helper: Loads a .conf / .ini file and returns a flat dictionary.
    
    - Booleans ('true'/'false' case-insensitive) → bool
    - Numbers (with or without decimal) → int or float
    - Everything else → str (whitespace stripped, empty → '')
    - All sections are flattened — no nesting preserved
    - Interpolation (%(name)s) is resolved automatically by configparser
    
    Usage in other projects:
        settings = load_configparser_flat('settings.conf')
        USR.update(settings)
    """
    path = Path(path)
    if not path.is_file():
        return {}

    cfg = configparser.ConfigParser(allow_no_value=True, interpolation=configparser.ExtendedInterpolation())
    read_files = cfg.read(path)
    if not read_files:
        return {}

    flat = {}
    for section in cfg.sections():
        for key, value in cfg[section].items():
            # Handle empty values
            if value is None or value.strip() == '':
                flat[key] = ''
                continue

            val = value.strip()

            # Boolean
            if val.lower() in ('true', 'false', 'yes', 'no', 'on', 'off'):
                flat[key] = val.lower() in ('true', 'yes', 'on')

            # Number (int or float)
            else:
                try:
                    if '.' in val or 'e' in val.lower() or 'E' in val:
                        flat[key] = float(val)
                    else:
                        flat[key] = int(val)
                except ValueError:
                    flat[key] = val  # keep as string

    return flat


def load_USR_defaults():
    """
    Creates user config if missing, reads user_conf.conf using configparser,
    updates USR with flat dictionary.
    """
    config_dir = Path.home() / '.config' / 'widelands_autokey'
    config_file = config_dir / 'user_conf.conf'

    config_dir.mkdir(parents=True, exist_ok=True)

    template_file = Path(__file__).parent / '.config_template' / 'user_conf.conf'

    # Copy template if user config missing
    if not config_file.exists():
        if template_file.exists():
            shutil.copy(template_file, config_file)
            print(f"Created user config: {config_file}")
        else:
            print(f"Template missing: {template_file}")
            print("Cannot continue — exiting.")
            sys.exit(1)

    # Load and flatten
    try:
        settings_dict = load_configparser_flat(config_file)

        # If sound_files section exists, store it as a nested dict
        # (this is the only place where we do something special)
        cfg = configparser.ConfigParser()
        cfg.read(config_file)
        if 'sound_files' in cfg:
            settings_dict['sound_files'] = dict(cfg['sound_files'])

        USR.update(settings_dict)
        USR['work_path'] = os.path.join(USR['work_path'], "")
        #print(USR['work_path'] , 'snot gobbler')
        if not os.path.exists(USR['work_path']):
            os.mkdir(USR['work_path'])
        USR['transient_path'] = os.path.join(USR['work_path'], 'autokey_transient_store.json')
    except Exception as e:
        print(f"ERROR: user_conf.conf is corrupt or invalid: {e}")
        print("Fallback: Manually copy template to overwrite your config file.")
        print(f"Template location: {template_file}")
        print(f"Target location: {config_file}")
        print("1. Copy the template file to the target location")
        print("2. Edit the copied file with your settings")
        print("3. Reload AutoKey")
        sys.exit(1)
