
# widelands/core.py
# ────────────────────────────────────────────────────────────────
# Single entry point for all AutoKey hotkeys.
# Loads ONLY the required tribe module on first use.
# ────────────────────────────────────────────────────────────────
#
# Version 2025 12 30

#import importlib
import os
import sys
import time
import json
import subprocess
import pyautogui
from statistics import mean
from math import sqrt
import io
from PIL import Image
from datetime import datetime
from Xlib import display, X
from Xlib.ext import xtest
from mss import mss

disp = display.Display()
root = disp.screen().root

try:# My personal stuff autokey module.
    import p2autokeym
    HAS_P2AUTOKEYM = True
except ImportError:
    HAS_P2AUTOKEYM = False

DEBUG = True
#DEBUG = False

CONTEXT = {
    'tribe': None,
    'keyboard': None,
    'building': None,
    'icon': None,
    'start_pos': None,
}


from widelands.current_tribe import get_tribe
get_tribe()# Defines the CONTEXT['tribe'] == to Amazon or Empire or whatevers

tribe = CONTEXT['tribe'].lower().strip()


# Make sure the parent directory is findable
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(PACKAGE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

# ────────────────────────────────────────────────
# Tribe loading
# ────────────────────────────────────────────────

from widelands.current_tribe import get_tribe
get_tribe()

tribe = CONTEXT.get('tribe')
if not tribe:
    print("ERROR: Tribe not detected after get_tribe()!", file=sys.stderr)
else:
    tribe = tribe.lower().strip()
    tribe_module_name = f"widelands.tribes.{tribe}"

    try:
        # Modern Python 3: use importlib (cleaner than __import__)
        import importlib
        mod = importlib.import_module(tribe_module_name)

        # Copy public names into globals
        for name in dir(mod):
            if not name.startswith('__'):
                globals()[name] = getattr(mod, name)

        print(f"Loaded tribe: {tribe_module_name}")
    except ImportError as e:
        print(f"Failed to load tribe '{tribe_module_name}': {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error loading tribe: {e}", file=sys.stderr)





MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

NOTIFICATIONS_DIR = os.path.normpath(
    os.path.join(MODULE_DIR, '..','..', 'Sounds', 'Application', 'Notification')
)+'/'

PLAY_SOUND = {'red':NOTIFICATIONS_DIR+'bell.oga',
              'orange':NOTIFICATIONS_DIR+'complete.oga',
              'green':NOTIFICATIONS_DIR+'dialog-warning.oga',
              'big_error':NOTIFICATIONS_DIR+'phone-incoming-call.oga',
              'meedmeep':NOTIFICATIONS_DIR+'MeebMeeb.ogg',
              'down1':NOTIFICATIONS_DIR+'KDE_Window_Close.ogg',
              'up1':NOTIFICATIONS_DIR+'KDE_Window_Open.ogg',
              'down2':NOTIFICATIONS_DIR+'Chatdown.ogg',
              'up2':NOTIFICATIONS_DIR+'Chatup.ogg',
              'down3':NOTIFICATIONS_DIR+'Musica Restore Down.ogg',
              'up3':NOTIFICATIONS_DIR+'Musica Restore Up.ogg',
              'sharpstrum1':NOTIFICATIONS_DIR+'sharp_organ.ogg',
              }

def _play_sound(result):
    try:
        path = PLAY_SOUND.get(result, PLAY_SOUND['sharpstrum1'])
        subprocess.Popen(["paplay", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print(f'sound issues? {result}')  # fail — no sound




def simple_tst(key,keyboard):
    _play_sound('red')
    
