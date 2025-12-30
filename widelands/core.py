
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
globals().update(
    __import__(f".tribes.{tribe}", fromlist=["*"], package=__package__).__dict__
)








MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

NOTIFICATIONS_DIR = os.path.normpath(
    os.path.join(MODULE_DIR, '..', 'Sounds', 'Application', 'Notification')
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
