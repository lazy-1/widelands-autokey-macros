
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
import json
import importlib
import subprocess
import time
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


# Make sure the parent directory is findable
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(PACKAGE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

# ────────────────────────────────────────────────
# Tribe loading
# ────────────────────────────────────────────────
def import_tribe():
    from widelands.current_tribe import get_tribe
    get_tribe()

    tribe = CONTEXT.get('tribe').lower()
    if not tribe:
        print("ERROR: Tribe not detected after get_tribe()!", file=sys.stderr)
    else:
        tribe = tribe.lower().strip()
        tribe_module_name = f"widelands.tribes.{tribe}"

        try:
            # Modern Python 3: use importlib (cleaner than __import__)
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
import_tribe()






NOTIFICATIONS_DIR = os.path.normpath(
    os.path.join(PACKAGE_DIR, '..','..', 'Sounds', 'Application', 'Notification')
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

WORK_PATH = '/dev/shm/Widelands/'

if not os.path.exists(WORK_PATH):
    os.mkdir(WORK_PATH)
    
AUTOKEY_TOGGLE_FILE = WORK_PATH+'autokey_transient_store.json'

def debug_save_shm_append(text):
    with open(WORK_PATH+f"{CONTEXT['race']}_debug.txt", "a") as file:
        file.write(text)

def call_shortcut(key, keyboard):
    CONTEXT['keyboard'] = keyboard
    func_name = f"{key}"  # e.g., 'F1'
    func = globals().get(func_name)
    if func and callable(func):
        func()
    else:
        _play_sound('big_error')
        if HAS_P2AUTOKEYM:
            p2autokeym.dbus_send_FM('Widelands','TEXT',{'Error': f"Missing {func_name}","tribe": CONTEXT['tribe']})
        else:
            print(f"Missing {func_name}  {CONTEXT['tribe']}")
            
def _set_io(keyboard, building, icon):
    global CONTEXT
    CONTEXT['building'] = building
    CONTEXT['icon'] = icon

def stable_click(button=1):
    """
    Reliable replacement for mouse.click_relative_self(0, 0, button)
    
    Fixes Widelands 1.3 FieldActionWindow offset/double-click issues
    by stabilizing cursor position and using XTest fake events.
    
    Usage:
        stable_click()     → left click (default)
        stable_click(3)    → right click
    """
    # Get current real pointer position
    data = root.query_pointer()
    x, y = data.root_x, data.root_y
    
    # Warp to exact same position — stabilizes SDL2 multi-polls
    root.warp_pointer(x, y)
    disp.sync()
    
    # Minimal reliable settle — tune once per system (0.05–0.1 safe range)
    time.sleep(0.04)
    
    # Send clean press
    xtest.fake_input(disp, X.ButtonPress, button)
    disp.sync()
    time.sleep(0.02)  # Short realistic hold — can go down to 0.01 if stable
    
    # Send release
    xtest.fake_input(disp, X.ButtonRelease, button)
    disp.sync()


def stable_click_relative(dx=0, dy=0, button=1):
    """
    Clicks relative to current position WITHOUT warping back to absolute.
    Perfect for menu item selection after opening a dialog.
    """
    # Get current position
    data = root.query_pointer()
    current_x = data.root_x
    current_y = data.root_y
    
    # Calculate target position
    target_x = current_x + dx
    target_y = current_y + dy
    
    # Warp to the relative offset
    root.warp_pointer(target_x, target_y)
    disp.sync()
    time.sleep(0.05)  # Small settle — less than absolute click
    
    # Fake click at the new position
    xtest.fake_input(disp, X.ButtonPress, button)
    disp.sync()
    time.sleep(0.03)
    xtest.fake_input(disp, X.ButtonRelease, button)
    disp.sync()

def capture_mouse_pos():
    """Returns current mouse position as (x, y) tuple"""
    data = root.query_pointer()
    return (data.root_x, data.root_y)

def restore_mouse_pos(pos):
    """Warps mouse back to previously captured position"""
    x, y = pos
    root.warp_pointer(x, y)
    disp.sync()
    time.sleep(0.02)  # Tiny settle


def transient_store_get(tag, default=None):
    # A json containing True False vars nessisary for road building 
    data = {}
    # Read existing data
    try:
        with open(AUTOKEY_TOGGLE_FILE, 'r') as f:
            data = json.load(f)
    except (IOError, ValueError):  # Python 2: FileNotFoundError -> IOError, JSONDecodeError -> ValueError
        pass
    # If tag doesn't exist, set default and write to file
    if tag not in data:
        data[tag] = default
        try:
            with open(AUTOKEY_TOGGLE_FILE, 'w') as f:
                json.dump(data, f)
                #subprocess.call(['notify-send', '-t', '2000', 'Transient Store', 'Initialized {} = {}'.format(tag, default)]) # for debugging
        except Exception as e:
            pass
        #subprocess.call(['notify-send', '-t', '2000', 'Get Error', 'Failed to write {} = {}: {}'.format(tag, default, str(e))]) # for debugging
    return data.get(tag, default)

def transient_store_set(tag, value):
    data = {}
    # Read existing data
    try:
        with open(AUTOKEY_TOGGLE_FILE, 'r') as f:
            data = json.load(f)
    except (IOError, ValueError):
        pass
    # Set new value
    data[tag] = value
    try:
        with open(AUTOKEY_TOGGLE_FILE, 'w') as f:
            json.dump(data, f)
            #subprocess.call(['notify-send', '-t', '2000', 'Transient Store', 'Set {} = {}'.format(tag, value)]) # for debugging
    except Exception as e:
        pass
    #subprocess.call(['notify-send', '-t', '2000', 'Set Error', 'Failed to write {} = {}: {}'.format(tag, value, str(e))]) # for debugging


def get_mouse_position():
    """Returns (x:str, y:str) using xdotool – 100% reliable in AutoKey"""
    raw = subprocess.check_output(["xdotool", "getmouselocation"])
    if isinstance(raw, bytes):
        text = raw.decode("utf-8")
    else:
        text = raw
    parts = text.split()
    x = parts[0].split(":")[1]
    y = parts[1].split(":")[1]
    return x, y

def output_error(message="Unknown error"):
    """
    Error handler: uses p2autokeym dbus if available, else simple print.
    """
    if HAS_P2AUTOKEYM:
        # Your personal dbus feedback
        p2autokeym.dbus_send_FM('Widelands','TEXT',{'site':'no colour returned','building type':CONTEXT['building'],'Colour_Variance':CONTEXT['icon'],'Info':message})
        _play_sound('big_error')
    else:
        # Fallback  no p2autokeym
        print(f"ERROR: {message}")
        # Optional: play a sound if you want audible feedback
        _play_sound('big_error')
    

def unpause_pause(delay=0.2):
    CONTEXT['keyboard'].send_keys("<pause>")
    time.sleep(delay)
    CONTEXT['keyboard'].send_keys("<pause>")


# Direct keysym for Left Ctrl
XK_Control_L = 0xffe3

# Get the actual keycode (integer) — extract from the first tuple
ctrl_keycode = disp.keysym_to_keycodes(XK_Control_L)[0][0]  # <-- [0][0] gets the int

def ctrl_press():
    xtest.fake_input(disp, X.KeyPress, ctrl_keycode)
    disp.sync()
    time.sleep(0.05)

def ctrl_release():
    xtest.fake_input(disp, X.KeyRelease, ctrl_keycode)
    disp.sync()

    

def Build_Zigzag_Road(keyboard):
    CONTEXT['keyboard'] = keyboard
    do = transient_store_get('widelands_zigzag_rd', False)
    
    if do:# End road
        transient_store_set('widelands_zigzag_rd', False)
        stable_click()                    
        time.sleep(0.05)
        unpause_pause()
    
    else:# Begin Road
        transient_store_set('widelands_zigzag_rd', True)
        stable_click()           # First: open dialog
        time.sleep(0.05)  # Wait for dialog to open and settle (tune 0.15–0.22)
        stable_click()         # Second: select road icon
        
def Build_Connect_Road(keyboard):
    do = transient_store_get('widelands_join_rd', False)
    CONTEXT['keyboard'] = keyboard
    if do:# End road
        ctrl_press()#ctrl_on()
        time.sleep(0.05)
        transient_store_set('widelands_join_rd', False)
        stable_click()              # final click to place the connection
        time.sleep(0.1)
        ctrl_release()#ctrl_off()
        unpause_pause()
    else:# Begin Road
        transient_store_set('widelands_join_rd', True)
        stable_click()              # open dialog / start road mode
        time.sleep(0.1)
        stable_click()              # select the “connect roads” option


def Build_New_Road(keyboard):
    do = transient_store_get('widelands_long_rd',False)
    CONTEXT['keyboard'] = keyboard
    if do:# End road
        transient_store_set('widelands_long_rd',False)
        ctrl_press()#ctrl_on()
        stable_click()
        time.sleep(0.01)
        stable_click()
        time.sleep(0.01)
        stable_click()
        time.sleep(0.05)
        ctrl_release()#ctrl_off()
        time.sleep(0.1)
        unpause_pause()
    else:# Begin Road
        transient_store_set('widelands_long_rd',True)
        stable_click()              # open dialog / start road mode
        time.sleep(0.05)
        stable_click()              # select the “roads” option



        
#  For build_item icons example
#
# eg (40,80) = (+40pxls across, +80pxls down) from mouse location.
#
#

def in_building_dialog(x,y):# For Dismantles & Upgrades etc
    ctrl_press()#ctrl_on()'
    if DEBUG:
        time.sleep(0.02)
        get_screenshot_info(x=x,y=y,desc='in_building_dialog',area=(25,25))
        time.sleep(0.05)
    stable_click_relative(x, y) 
    time.sleep(0.05)
    ctrl_release()#ctrl_off()
    unpause_pause()
    stable_click(3)
    restore_mouse_pos(CONTEXT['start_pos'])


def build_item(x=0, y=0):# Current Tab
    if DEBUG:
        time.sleep(0.02)# race issues, mss is so fast....
        get_screenshot_info(x=x,y=y,desc='destination_click',area=(60,60))
        time.sleep(0.03)# race issues, mss is so fast....
    stable_click_relative(x, y)
    stable_click(3)
    unpause_pause(0.15)

def build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg):
    if DEBUG:
        time.sleep(0.02)# race issues, mss is so fast....
        get_screenshot_info(x=x_tab,y=y_tab,desc='tab_selection',area=(40,40))
        time.sleep(0.03)# race issues, mss is so fast....
    stable_click_relative(x_tab,y_tab)
    time.sleep(0.02)
    if DEBUG:
        time.sleep(0.02)# race issues, mss is so fast....
        get_screenshot_info(x=x_bldg,y=y_bldg,desc='build_selection',area=(60,60))
        time.sleep(0.03)# race issues, mss is so fast....
    stable_click_relative(x_bldg, y_bldg)
    unpause_pause(0.15)
    stable_click(3)
    
def build_item_M_S(x_bldg, y_bldg): # Move Medium to Small Tab
    x_tab, y_tab = (-35, 0)
    build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg)
    
def build_item_L_S(x_bldg, y_bldg): # Move Large to Small Tab
    x_tab, y_tab = (-70, 0)
    build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg)

def build_item_L_M(x_bldg, y_bldg): # Move Large to Medium Tab
    x_tab, y_tab = (-35, 0)
    build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg)

       
def analyze_dialog(building): #For build sites mainly
    # 1. Open the dialog/window
    CONTEXT['start_pos'] = capture_mouse_pos()
    stable_click()
    time.sleep(0.03)  # Let it fully render
    build, site, variance = get_screenshot_info(desc=building)
    return build, site

def determine_dialog():# For a built building what is it?
    # 1. Open the dialog/window
    CONTEXT['start_pos'] = capture_mouse_pos()
    stable_click()
    time.sleep(0.09)  # Let it fully render
    build,site,var = get_screenshot_info(x=-62,y=-35,area=(30,17),
                                         method='building')
    if site == 'Standard_brown':
        build,site,var = get_screenshot_info(x=-327,y=-67,area=(22,22),
                                             method='building')
    #if site == 'none':
        
    return site

def get_screenshot_info(x=0, y=0, desc='n-a', area=(29, 29), method='general'):
    # Unpack width/height
    width, height = area
    half_w = width // 2
    half_h = height // 2
    
    # Get current mouse position
    x_str, y_str = get_mouse_position()
    mouse_x, mouse_y = int(x_str), int(y_str)

    # Apply offset
    capture_x = mouse_x + x - half_w
    capture_y = mouse_y + y - half_h

    try:
        with mss() as sct:
            monitor = {
                "left": capture_x,
                "top": capture_y,
                "width": width,
                "height": height
            }
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

    except Exception as e:
        print(f"Screenshot failed: {e}")
        _play_sound('big_error')
        return False, 'none', 0

    # Rest of your code remains identical
    pixels = [p[:3] for p in img.getdata()]
    n = len(pixels)
    if n == 0:
        print("No pixels in snapshot")
        return False, 'none', 0

    r = sum(p[0] for p in pixels) // n
    g = sum(p[1] for p in pixels) // n
    b = sum(p[2] for p in pixels) // n

    variance = sum((p[0]-r)**2 + (p[1]-g)**2 + (p[2]-b)**2 for p in pixels) / n

    # Call the appropriate classifier
    if method == 'general':
        build, site = id_site_tab_color(r, g, b, variance)
    elif method == 'building':
        build, site = id_building_via_dialog_tells(r, g, b, variance)
    elif method == 'id_dialog_icon':
        build, site = id_dialog_icon(r, g, b, variance)
    else:
        build, site = False, "None"

    # Timestamp and info string 
    timestamp = datetime.now().strftime("%H%M%S_%f")[:-4]
    info = f"{timestamp}_{desc}-{ 'T' if build else 'F' }-{site}-{str(int(variance))}_RGB{r:03d}_{g:03d}_{b:03d}"

    if DEBUG:
        filename = f"{WORK_PATH}{info}.png"
        img.save(filename)

    debug_save_shm_append(info + '\n')

    return build, site, variance


def id_site_tab_color(r, g, b, variance):
    # IF you need more tests brightness is an option..
    # brightness = (r + g + b) // 3

    # RED tab — wider tolerance + low variance
    if (abs(r - 98) <= 10 and abs(g - 26) <= 8 and abs(b - 18) <= 8
        and variance < 8000):
        return (True, 'red')

    # ORANGE tab — tighter tolerance + low variance
    if (abs(r - 136) <= 5 and abs(g - 72) <= 5 and abs(b - 11) <= 5
        and variance < 12000):
        return (True, 'orange')

    # GREEN tab — tighter tolerance + low variance
    if (abs(r - 18) <= 5 and abs(g - 87) <= 5 and abs(b - 8) <= 5
        and variance < 6000):
        return (True, 'green')

    if (abs(r - 27) <= 5 and abs(g - 68) <= 5 and abs(b - 95) <= 5
        and variance < 8500):
        return (True, 'blue')# Seafaring 

    return id_dialog_icon(r, g, b, variance)




    






