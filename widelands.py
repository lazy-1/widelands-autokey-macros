# 2025 12 28
# A module for Widelands.
#
# widelands.py  –  Widelands-specific functions only

#

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

# My personal stuff, comment it out and use your own feedback

try:# My personal stuff autokey module.
    import p2autokeym
    HAS_P2AUTOKEYM = True
except ImportError:
    HAS_P2AUTOKEYM = False

DEBUG = True
DEBUG = False


    
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
        print('sound issues?')  # fail — no sound



CONTEXT = {
    'race': None,
    'keyboard': None,
    'building': None,
    'icon': None,
    'start_pos': None,
    # Add more later if needed
}




WORK_PATH = '/dev/shm/Widelands/'

if not os.path.exists(WORK_PATH):
    os.mkdir(WORK_PATH)


AUTOKEY_TOGGLE_FILE = WORK_PATH+'autokey_transient_store.json'



def _set_io(keyboard, building, icon):
    global CONTEXT
    CONTEXT['keyboard'] = keyboard
    CONTEXT['building'] = building
    CONTEXT['icon'] = icon


    
def race():
    num,race = 0,''
    if num == 0:race = 'Amazon'
    elif num == 1:race = 'Atlantean'
    elif num == 2:race = 'Barbarian'
    elif num == 3:race = 'Empire'
    elif num == 4:race = 'Frisian'
    CONTEXT['race'] = race
    return race

def debug_save_shm_append(text):
    with open(WORK_PATH+'debug_building_col.txt', "a") as file:
        file.write(text)








# These should already be in your script — keep them at the very top
disp = display.Display()
root = disp.screen().root

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
    time.sleep(0.04)  # Minimal reliable settle — tune once per system (0.05–0.1 safe range)
    
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
    
    # OPTIONAL: warp back to original position if desired
    # (Usually not needed — mouse stays where user expects: on the menu item)
    # root.warp_pointer(current_x, current_y)
    # disp.sync()


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
                #subprocess.call(['notify-send', '-t', '2000', 'Transient Store', 'Initialized {} = {}'.format(tag, default)])
        except Exception as e:
            pass
        #subprocess.call(['notify-send', '-t', '2000', 'Get Error', 'Failed to write {} = {}: {}'.format(tag, default, str(e))])
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
            #subprocess.call(['notify-send', '-t', '2000', 'Transient Store', 'Set {} = {}'.format(tag, value)])
    except Exception as e:
        pass
    #subprocess.call(['notify-send', '-t', '2000', 'Set Error', 'Failed to write {} = {}: {}'.format(tag, value, str(e))])


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




#
#  For Notepad icons example
#
# eg (40,80) = (+40pxls across, +80pxls down)
#
#


def build_item(x=0, y=0):# Current Tab
    if DEBUG:
        get_screenshot_info(desc='mouse_open_pos',size=50)
        get_screenshot_info(x=x,y=y,desc='destination_click',size=50)
    stable_click_relative(x, y)
    stable_click(3)
    unpause_pause(0.15)

def build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg):
    if DEBUG:
        get_screenshot_info(desc='mouse_open_pos',size=50)
        get_screenshot_info(x=x_tab,y=y_tab,desc='tab_selection',size=50)
    stable_click_relative(x_tab,y_tab)
    time.sleep(0.02)
    if DEBUG:
        get_screenshot_info(x=x_bldg,y=y_bldg,desc='build_selection',size=60)
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




def err_no_col(message="Unknown error"):
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
    


def in_building_dialog(x,y):# For Dismantles & Upgrades
    ctrl_press()#ctrl_on()'
    if DEBUG:
        get_screenshot_info(x=x,y=y,desc='in_building_dialog',size=21)
    stable_click_relative(x, y) 
    time.sleep(0.05)
    ctrl_release()#ctrl_off()
    unpause_pause()
    stable_click(3)
    restore_mouse_pos(CONTEXT['start_pos'])







    
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
    _set_io(keyboard, None, None) 
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
    _set_io(keyboard, None, None) 
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
    _set_io(keyboard, None, None) 
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

    
def call_shortcut(key, keyboard):
    race_str = race()
    func_name = f"{race_str}_{key}"  # e.g., 'Atlantean_F1'
    func = globals().get(func_name)
    if func and callable(func):
        func(keyboard)
    else:
        _play_sound('big_error')
        if HAS_P2AUTOKEYM:
            p2autokeym.dbus_send_FM('Widelands','TEXT',{'Error': f"Missing {func_name}"})
        else:
            print(f"Missing {func_name}")


            
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
    time.sleep(0.03)  # Let it fully render
    build,site,var = get_screenshot_info(x=-68,y=-35,size=17,
                                         method='building')
    if site == 'Standard_brown':
        build,site,var = get_screenshot_info(x=-327,y=-67,size=21,
                                             method='building')
    return site





def get_screenshot_info(x=0, y=0, desc='n-a', size=29, method='general'):
    # Get current mouse position
    x_str, y_str = get_mouse_position() 
    x, y = int(x_str) + x, int(y_str) + y
    half = size // 2

    try:
        with mss() as sct:
            monitor = {"left": x - half, "top": y - half, "width": size, "height": size}
            sct_img = sct.grab(monitor)
            # Convert to PIL Image (RGB)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

    except Exception as e:
        print(f"Screenshot failed: {e}")
        _play_sound('big_error')
        return False, 'none', 0

    # Calculate average RGB
    pixels = [p[:3] for p in img.getdata()]
    n = len(pixels)
    if n == 0:
        print("No pixels in snapshot")
        return False, 'none', 0

    r = sum(p[0] for p in pixels) // n
    g = sum(p[1] for p in pixels) // n
    b = sum(p[2] for p in pixels) // n

    variance = sum((p[0]-r)**2 + (p[1]-g)**2 + (p[2]-b)**2 for p in pixels) / n

    # Call the appropriate classifier (exactly as original)
    if method == 'general':
        build, site = classify_tab_color(r, g, b, variance)
    elif method == 'building':
        build, site = classify_building(r, g, b, variance)
    elif method == 'modify':
        build, site = classify_dialog(r, g, b, variance)
    else:
        build, site = False, "None"

    # Timestamp and info string (exactly as original)
    timestamp = datetime.now().strftime("%H%M%S_%f")[:-4]
    info = f"{timestamp}_{desc}-{ 'T' if build else 'F' }-{site}-{str(int(variance))}_RGB{r:03d}_{g:03d}_{b:03d}"

    if DEBUG:
        filename = f"{WORK_PATH}{info}.png"
        img.save(filename)

    debug_save_shm_append(info + '\n')

    return build, site, variance

















def OLDget_screenshot_info(x=0,y=0,desc='n-a',size=29,method='general'):
    #  Get current mouse position
    x_str, y_str = get_mouse_position() 
    x, y = int(x_str)+x, int(y_str)+y
    half = size // 2
    try:
        img = pyautogui.screenshot(region=(x - half, y - half, size, size))
    except Exception as e:
        print(f"Screenshot failed: {e}")
        _play_sound('big_error')
        return False, 'none', 0
    
    #  Calculate average RGB
    pixels = [p[:3] for p in img.getdata()]
    n = len(pixels)
    if n == 0:
        print("No pixels in snapshot")
        return

    r = sum(p[0] for p in pixels) // n
    g = sum(p[1] for p in pixels) // n
    b = sum(p[2] for p in pixels) // n

    variance = sum((p[0]-r)**2 + (p[1]-g)**2 + (p[2]-b)**2 for p in pixels) / n
    if method == 'general':
        build, site = classify_tab_color(r, g, b, variance)
    elif method == 'building':
        build, site = classify_building(r, g, b, variance)
    elif method == 'modify':
        build, site = classify_dialog(r, g, b, variance)
    else:
        build, site = "None"
    timestamp = datetime.now().strftime("%H%M%S_%f")[:-4]
    info = f"{timestamp}_{desc}-{ 'T' if build else 'F' }-{site}-{str(int(variance))}_RGB{r:03d}_{g:03d}_{b:03d}"
    if DEBUG:
        # Save snapshot with timestamp + RGB in filename
        filename = f"{WORK_PATH}{info}.png"
        img.save(filename)

    debug_save_shm_append(info+'\n')
    return build, site, variance
    


def classify_tab_color(r, g, b, variance):
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
    
    return classify_dialog(r, g, b, variance)

def classify_dialog(r, g, b, variance):
    # Built Building Dialogs
    race = CONTEXT['race']
    if race == 'Amazon':
        if (abs(r - 107) <= 5 and abs(g - 76) <= 5 and abs(b - 48) <= 5
            and variance < 11000):
            return (False, 'swirl')
        if (abs(r - 113) <= 5 and abs(g - 84) <= 5 and abs(b - 45) <= 5
            and variance < 3500):
            return (False, 'Charcoal')

        if (abs(r - 98) <= 5 and abs(g - 72) <= 5 and abs(b - 55) <= 5
            and variance < 6000):
            return (False, 'remove_worker')

        if (abs(r - 104) <= 5 and abs(g - 82) <= 5 and abs(b - 55) <= 5
            and variance < 800):
            return (False, 'upgrade_icon')

        if (abs(r - 97) <= 5 and abs(g - 77) <= 5 and abs(b - 47) <= 5
            and variance < 700):
            return (False, 'upgrade_icon')


        if (abs(r - 85) <= 2 and abs(g - 76) <= 2 and abs(b - 15) <= 2
            and 12000 < variance < 13500):
            return (False, 'building_built')#is a woodcutter or Jungle preserve



        

    elif race == 'Atlantean':
        pass

    elif race == 'Barbarian':
        pass
    elif race == 'Empire':
        pass
    elif race == 'Frisian':
        pass
    
    return (False, f"({r}, {g}, {b}, {int(variance)})")  
    
 
def classify_building(r, g, b, variance):
    # Built Building Dialogs
    race = CONTEXT['race']
    if race == 'Amazon':
        if (abs(r - 120) <= 10 and abs(g - 110) <= 10 and abs(b - 31) <= 10
            and 10000 < variance < 12500):# Ga image
            return (False, 'Garrison')
        
        if (abs(r - 86) <= 5 and abs(g - 66) <= 5 and abs(b - 38) <= 5
            and 250 < variance < 500):# Blank brown image
            return (False, 'Standard_brown')
        
        if (abs(r - 96) <= 3 and abs(g - 76) <= 3 and abs(b - 45) <= 3
            and 250 < variance < 450):# Blank brown image
            return (False, 'Lighter_brown')
        
        if (abs(r - 67) <= 5 and abs(g - 51) <= 5 and abs(b - 25) <= 5
            and 1000 < variance < 2000):# Tiny Liana icon
            return (False, 'Liana')

        if (abs(r - 70) <= 5 and abs(g - 58) <= 5 and abs(b - 40) <= 5
            and 3000 < variance < 4000):# Tiny StoneCutter icon
            return (False, 'Stonecutter')

        if (abs(r - 112) <= 5 and abs(g - 87) <= 5 and abs(b - 60) <= 5
            and 9000 < variance < 10500):# Tiny Woodcutter icon
            return (False, 'Woodcutter')
        
    elif race == 'Atlantean':
        pass

    elif race == 'Barbarian':
        pass
    elif race == 'Empire':
        pass
    elif race == 'Frisian':
        pass
    
    return (False, f"({r}, {g}, {b}, {int(variance)})")  
    



    
        
# Amazon
# ===============================================
# Amazon — FUNCTIONS (F1–F12 + end + hyphen + equal + backslash + rightbracket)
# ===============================================

"""

# pip install mss
from mss import mss
with mss() as sct:
    img = sct.grab({"left": x-half, "top": y-half, "width": size, "height": size})
    img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")




"""



def Amazon_F1(keyboard):
    btype = 'Stonecutter'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (10, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Amazon_F2(keyboard):
    btype = 'Woodcutter'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if build:
        item_pos = (60, 45) 
        if site == 'red':
            build_item(*item_pos)
        elif site == 'orange':
            build_item_M_S(*item_pos)
        elif site == 'green':
            build_item_L_S(*item_pos)
        return
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)

    
    _, built, var = get_screenshot_info(x=0,y=-90,desc='detect_dialog',size=15)

    if site == 'swirl':
        if built == 'building_built':#, 'remove_worker'
            in_building_dialog(68, -34)
            return
            
  
    err_no_col(f'{built} toggled-{toggle_tab}')


def Amazon_F3(keyboard):
    btype = 'Jungle_Preserve'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if build:
        item_pos = (105, 45)
        if site == 'red':
            build_item(*item_pos)
        elif site == 'orange':
            build_item_M_S(*item_pos)
        elif site == 'green':
            build_item_L_S(*item_pos)
        else:
            err_no_col()
        return
    _, built, var = get_screenshot_info(x=0,y=-90,desc='detect_dialog',size=15)
    if site == 'swirl': # remove worker
        
        in_building_dialog(68, -34, 'remove_worker')
        
    


def Amazon_F4(keyboard):
    btype = 'Water_Gatherer'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (10, 95)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Amazon_F5(keyboard):
    btype = 'Cassava_Root_Cooker'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (75, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)  # GREEN → medium tab
    else:
        err_no_col()

def Amazon_F6(keyboard):
    btype = 'Chocolate_Brewery'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (125, 95)  # corrected from 125 → 95 to match actual position
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)
    else:
        err_no_col()

def Amazon_F7(keyboard):
    btype = 'Charcoal_Kiln'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    if toggle_tab:# infinate Production of charcoal
        start_pos = capture_mouse_pos()
        in_building_dialog(-175, 20)
        stable_click(3)  # right-click
        restore_mouse_pos(start_pos)

    else:#'Charcoal_Kiln'
        item_pos = (25, 95)
        if site == 'orange':
            build_item(*item_pos)
        elif site == 'green':
            build_item_L_M(*item_pos)
        else:
            err_no_col()

def Amazon_F8(keyboard):
    btype = 'Food_Preserver'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (175, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)
    else:
        err_no_col()

def Amazon_F9(keyboard):
    btype = 'DressMakery'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (-25, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)
    else:
        err_no_col()

def Amazon_F10(keyboard):
    btype = 'Rare_Tree_Plantation'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    if toggle_tab:  #  Infinate Rare Tree Production
        start_pos = capture_mouse_pos()
        in_building_dialog(-285, 0) 
        stable_click(3)
        unpause_pause(0.02)
        restore_mouse_pos(start_pos)
    else: #  # Build Site
        item_pos = (125, 50)
        if site == 'orange':
            build_item(*item_pos)
        elif site == 'green':
            build_item_L_M(*item_pos)
        else:
            err_no_col()

def Amazon_F11(keyboard):
    btype = 'Hunter_Gatherer'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (160, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Amazon_F12(keyboard):
    btype = 'Wilderness_Keeper'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (60, 95)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()


def Amazon_end(keyboard):
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    btype = 'Furnace' if toggle_tab else 'Stone_Workshop'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)

    # Toggle changes only the item position
    item_pos = (75, 50) if toggle_tab else (175, 45)

    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)
    else:
        err_no_col()

def Amazon_plus(keyboard):
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    btype = 'Rope_Weaver' if toggle_tab else 'Liana_Cutter'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)

    # Toggle changes only the item position
    item_pos = (25, 45) if toggle_tab else (205, 45)
    if toggle_tab:#'Rope_Weaver'
        if site == 'orange':
            build_item(*item_pos)
        elif site == 'green':
            build_item_L_M(*item_pos)
        else:
            err_no_col()
    else:#'Liana_Cutter'
        if site == 'red':
            build_item(*item_pos)
        elif site == 'orange':
            build_item_M_S(*item_pos)
        elif site == 'green':
            build_item_L_S(*item_pos)
        else:
            err_no_col()

def Amazon_equal(keyboard):
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    btype = 'Warriors_Dwelling' if toggle_tab else 'Tower'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)

    # Toggle changes only the item position
    #      'Warriors_Dwelling'     else     'Tower' (default)
    item_pos = (125, 145) if toggle_tab else (175, 145)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)
    else:
        err_no_col()

def Amazon_hyphen(keyboard):
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    
    if toggle_tab:  # Upgrade_to_Rare — special case (dismantle + right-click)
        pass
    else:  # Patrol_Post — normal build
        btype = 'Patrol-Post'
        build, site = analyze_dialog(btype)
        _set_io(keyboard, btype, site)
        item_pos = (160, 95)

        if site == 'red':
            build_item(*item_pos)
        elif site == 'orange':
            build_item_M_S(*item_pos)
        elif site == 'green':
            build_item_L_S(*item_pos)
        else:
            err_no_col()






def Amazon_scroll_lock(keyboard):
    _set_io(keyboard, 'Amazon_scroll_lock_Destroy', 'none')
    site = determine_dialog()
    if site == 'Garrison':
        in_building_dialog(-164,0)
    if site == 'Liana':
        in_building_dialog(-235,0)
    if site == 'Stonecutter':
        in_building_dialog(-275, 0)
    if site == 'Woodcutter':
        in_building_dialog(-205, 0)

    
def Amazon_backslash(keyboard):
    # Dismantle Sites..
    _set_io(keyboard, 'Amazon_backslash_Dismantle', 'none')
    site = determine_dialog()
    if site == 'Garrison':
        in_building_dialog(-124,0)
    if site == 'Liana':
        in_building_dialog(-195,0)
    if site == 'Stonecutter':
        in_building_dialog(-235, 0)
    if site == 'Woodcutter':
        in_building_dialog(-165, 0)
    
def Amazon_rightbracket(keyboard):
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    _set_io(keyboard, 'Amazon_rightbracket', 'none')
    if toggle_tab:  # 
        pass
    else:
        # Double Click
        stable_click()
        time.sleep(0.1)
        stable_click()
        unpause_pause(0.1)

def Amazon_leftbracket(keyboard):
    _set_io(keyboard, 'Amazon_leftbracket', 'none')
    site = determine_dialog()
    if site == 'Garrison':
        _, usite, var = get_screenshot_info(x=-188,y=0,
                                         method='modify')
        if usite == 'upgrade_icon':
            in_building_dialog(-188,0)
    if site == 'Woodcutter':
        in_building_dialog(-234, 0)
    if site == 'Lighter_brown':
        in_building_dialog(-206, 0)
        

    return
    _, built, var = get_screenshot_info(x=0,y=-90,desc='detect_dialog',size=15)
    if built == 'woodcutter_built':
        if site == 'swirl':
            if toggle_tab:  
                in_building_dialog(-234, 0,'upgrade_built_building')
                return
            else:
                in_building_dialog(68, -34, 'remove_worker')
                return
    else:
        if site == 'swirl': # 'Upgrade_to_Rare_unbuilt'
                in_building_dialog(-210, 0,'upgrade_unbuilt_building')
                return



# Atlantean

# ===============================================
# Atlantean FUNCTIONS (F1–F12 + end + hyphen + equal + backslash + rightbracket)
# ===============================================

def Atlantean_F1(keyboard):
    btype = 'Quarry'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (5, 40)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F2(keyboard):
    btype = 'Woodcutter'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (60, 45)  # standardised Y to match most buildings
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F3(keyboard):
    btype = 'Forester'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (105, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F4(keyboard):
    btype = 'Well'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (55, 95)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F5(keyboard):
    btype = 'Bakery'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (175, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F6(keyboard):
    btype = 'Smokery'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (75, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F7(keyboard):
    btype = 'Mill'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (125, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F8(keyboard):
    btype = 'Smelter'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (20, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F9(keyboard):
    btype = 'Weaponsmith'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (125, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F10(keyboard):
    btype = 'Armoursmith'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (175, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F11(keyboard):
    btype = 'Fish'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (155, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F12(keyboard):
    btype = 'Fishbreader'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (205, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_end(keyboard):
    btype = 'SawMill'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (25, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_hyphen(keyboard):
    btype = 'Guardhouse'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (200, 100)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_equal(keyboard):
    btype = 'Tower'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (125, 135)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_backslash(keyboard):
    # Dismantle Guardhouse, Tower, Castle
    _set_io(keyboard, 'TypeA_Dismantle', 'none')
    in_building_dialog(-130, 0)

def Atlantean_rightbracket(keyboard):
    # Dismantle Woodcutter, Quarry
    _set_io(keyboard, 'TypeB_Dismantle', 'none')
    in_building_dialog(-235, 0)



# Barbarian

# ===============================================
# Barbarian  (F1–F12 + end + hyphen + equal + backslash + rightbracket)
# ===============================================


def Barbarian_F1(keyboard):
    btype = 'Quarry'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (5, 40)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F2(keyboard):
    btype = 'Woodcutter'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (60, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F3(keyboard):
    btype = 'Forester'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (105, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F4(keyboard):
    btype = 'Well'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (55, 95)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F5(keyboard):
    btype = 'Bakery'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (175, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F6(keyboard):
    btype = 'Smokery'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (75, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F7(keyboard):
    btype = 'Mill'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (125, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F8(keyboard):
    btype = 'Smelter'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (20, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F9(keyboard):
    btype = 'Weaponsmith'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (125, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F10(keyboard):
    btype = 'Armoursmith'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (175, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F11(keyboard):
    btype = 'Fish'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (155, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F12(keyboard):
    btype = 'Fishbreader'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (205, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_end(keyboard):
    btype = 'SawMill'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (25, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_hyphen(keyboard):
    btype = 'Guardhouse'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (200, 100)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_equal(keyboard):
    btype = 'Tower'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    item_pos = (125, 135)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_backslash(keyboard):
    # Dismantle Guardhouse, Tower, Castle
    _set_io(keyboard, 'TypeA_Dismantle', 'none')
    in_building_dialog(-130, 0)

def Barbarian_rightbracket(keyboard):
    # Dismantle Woodcutter, Quarry
    _set_io(keyboard, 'TypeB_Dismantle', 'none')
    in_building_dialog(-235, 0)






# Empire

# ===============================================
# Empire FUNCTIONS (F1–F12 + end + hyphen + equal + backslash + rightbracket)
# ===============================================


def Empire_F1(keyboard):
    btype = 'Quarry'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(5, 40)
    elif site == 'orange':
        notepd_tab_select(-35, 0, -25, 40)
    elif site == 'green':
        notepd_tab_select(-65, 0, -60, 40)
    else:
        err_no_col()

def Empire_F2(keyboard):
    btype = 'Woodcutter'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(60, 40)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 20, 55)
    elif site == 'green':
        notepd_tab_select(-65, 0, -10, 45)
    else:
        err_no_col()

def Empire_F3(keyboard):
    btype = 'Forester'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(105, 45)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 80, 45)
    elif site == 'green':
        notepd_tab_select(-65, 0, 40, 45)
    else:
        err_no_col()

def Empire_F4(keyboard):
    btype = 'Well'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(55, 95)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 25, 95)
    elif site == 'green':
        notepd_tab_select(-65, 0, -15, 95)
    else:
        err_no_col()

def Empire_F5(keyboard):
    btype = 'Bakery'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(175, 50)
    elif site == 'green':
        notepd_tab_select(-35, 0, 140, 50)
    else:
        err_no_col()

def Empire_F6(keyboard):
    btype = 'Smokery'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(75, 50)
    elif site == 'green':
        notepd_tab_select(-35, 0, 40, 50)
    else:
        err_no_col()

def Empire_F7(keyboard):
    btype = 'Mill'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(125, 50)
    elif site == 'green':
        notepd_tab_select(-35, 0, 95, 50)
    else:
        err_no_col()

def Empire_F8(keyboard):
    btype = 'Smelter'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(20, 95)
    elif site == 'green':
        notepd_tab_select(-35, 0, -15, 95)
    else:
        err_no_col()

def Empire_F9(keyboard):
    btype = 'Weaponsmith'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(125, 95)
    elif site == 'green':
        notepd_tab_select(-35, 0, 95, 95)
    else:
        err_no_col()

def Empire_F10(keyboard):
    btype = 'Armoursmith'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(175, 95)
    elif site == 'green':
        notepd_tab_select(-35, 0, 140, 95)
    else:
        err_no_col()

def Empire_F11(keyboard):
    btype = 'Fish'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(155, 45)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 120, 45)
    elif site == 'green':
        notepd_tab_select(-65, 0, 85, 45)
    else:
        err_no_col()

def Empire_F12(keyboard):
    btype = 'Fishbreader'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(205, 45)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 170, 45)
    elif site == 'green':
        notepd_tab_select(-65, 0, 140, 45)
    else:
        err_no_col()

def Empire_end(keyboard):
    btype = 'SawMill'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(25, 50)
    elif site == 'green':
        notepd_tab_select(-35, 0, -15, 50)
    else:
        err_no_col()

def Empire_hyphen(keyboard):
    btype = 'Guardhouse'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(200, 100)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 170, 100)
    elif site == 'green':
        notepd_tab_select(-65, 0, 140, 100)
    else:
        err_no_col()

def Empire_equal(keyboard):
    btype = 'Tower'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(125, 135)
    elif site == 'green':
        notepd_tab_select(-35, 0, 95, 135)
    else:
        err_no_col()

def Empire_backslash(keyboard):
    # Dismantle  Gaurdhouse, Tower, Castle
    _set_io(keyboard, 'TypeA_Dismantle', 'none')
    in_building_dialog(-130, 0)

def Empire_rightbracket(keyboard):
    # Dismantle Woodcutter, Quarry.
    _set_io(keyboard, 'TypeB_Dismantle', 'none')
    in_building_dialog(-235, 0)
 
    

# Frisian


# ===============================================
# FRISIAN FUNCTIONS (F1–F12 + end + hyphen + equal + backslash + rightbracket)
# ===============================================

def Frisian_F1(keyboard):
    btype = 'Quarry'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(5, 40)
    elif site == 'orange':
        notepd_tab_select(-35, 0, -25, 40)
    elif site == 'green':
        notepd_tab_select(-65, 0, -60, 40)
    else:
        err_no_col()

def Frisian_F2(keyboard):
    btype = 'Woodcutter'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(60, 40)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 20, 55)
    elif site == 'green':
        notepd_tab_select(-65, 0, -10, 45)
    else:
        err_no_col()

def Frisian_F3(keyboard):
    btype = 'Forester'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(105, 45)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 80, 45)
    elif site == 'green':
        notepd_tab_select(-65, 0, 40, 45)
    else:
        err_no_col()

def Frisian_F4(keyboard):
    btype = 'Well'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(55, 95)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 25, 95)
    elif site == 'green':
        notepd_tab_select(-65, 0, -15, 95)
    else:
        err_no_col()

def Frisian_F5(keyboard):
    btype = 'Bakery'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(175, 50)
    elif site == 'green':
        notepd_tab_select(-35, 0, 140, 50)
    else:
        err_no_col()

def Frisian_F6(keyboard):
    btype = 'Smokery'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(75, 50)
    elif site == 'green':
        notepd_tab_select(-35, 0, 40, 50)
    else:
        err_no_col()

def Frisian_F7(keyboard):
    btype = 'Mill'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(125, 50)
    elif site == 'green':
        notepd_tab_select(-35, 0, 95, 50)
    else:
        err_no_col()

def Frisian_F8(keyboard):
    btype = 'Smelter'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(20, 95)
    elif site == 'green':
        notepd_tab_select(-35, 0, -15, 95)
    else:
        err_no_col()

def Frisian_F9(keyboard):
    btype = 'Weaponsmith'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(125, 95)
    elif site == 'green':
        notepd_tab_select(-35, 0, 95, 95)
    else:
        err_no_col()

def Frisian_F10(keyboard):
    btype = 'Armoursmith'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(175, 95)
    elif site == 'green':
        notepd_tab_select(-35, 0, 140, 95)
    else:
        err_no_col()

def Frisian_F11(keyboard):
    btype = 'Fish'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(155, 45)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 120, 45)
    elif site == 'green':
        notepd_tab_select(-65, 0, 85, 45)
    else:
        err_no_col()

def Frisian_F12(keyboard):
    btype = 'Fishbreader'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(205, 45)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 170, 45)
    elif site == 'green':
        notepd_tab_select(-65, 0, 140, 45)
    else:
        err_no_col()

def Frisian_end(keyboard):
    btype = 'SawMill'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(25, 50)
    elif site == 'green':
        notepd_tab_select(-35, 0, -15, 50)
    else:
        err_no_col()

def Frisian_hyphen(keyboard):
    btype = 'Guardhouse'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'red':
        notepd_strait(200, 100)
    elif site == 'orange':
        notepd_tab_select(-35, 0, 170, 100)
    elif site == 'green':
        notepd_tab_select(-65, 0, 140, 100)
    else:
        err_no_col()

def Frisian_equal(keyboard):
    btype = 'Tower'
    build, site = analyze_dialog(btype)
    _set_io(keyboard, btype, site)
    if site == 'orange':
        notepd_strait(125, 135)
    elif site == 'green':
        notepd_tab_select(-35, 0, 95, 135)
    else:
        err_no_col()

def Frisian_backslash(keyboard):
    # Dismantle  Gaurdhouse, Tower, Castle
    _set_io(keyboard, 'TypeA_Dismantle', 'none')
    in_building_dialog(-130, 0)

def Frisian_rightbracket(keyboard):
    # Dismantle Woodcutter, Quarry.
    _set_io(keyboard, 'TypeB_Dismantle', 'none')
    in_building_dialog(-235, 0)
 
    
