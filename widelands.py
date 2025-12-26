
# widelands.py  –  Widelands-specific functions only
#
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

import p2autokeym # My personal stuff, comment it out and use your own feedback



MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


NOTIFICATIONS_DIR = os.path.normpath(
    os.path.join(MODULE_DIR, '..', 'Sounds', 'Application', 'Notification')
)+'/'



PLAY_SOUND = {'RED':NOTIFICATIONS_DIR+'bell.oga',
              'ORANGE':NOTIFICATIONS_DIR+'complete.oga',
              'GREEN':NOTIFICATIONS_DIR+'dialog-warning.oga',
              'none':NOTIFICATIONS_DIR+'phone-incoming-call.oga',
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
    path = PLAY_SOUND.get(result, PLAY_SOUND['none'])
    #print(result,path)
    subprocess.Popen(["paplay", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


KEYBOARD = BUILDING = ICON = None



DEBUG = True
DEBUG = False


WORK_PATH = '/dev/shm/Widelands/'

if not os.path.exists(WORK_PATH):
    os.mkdir(WORK_PATH)


AUTOKEY_TOGGLE_FILE = WORK_PATH+'autokey_transient_store.json'



def _set_io(keyboard, building, icon):
    global KEYBOARD, BUILDING, ICON
    KEYBOARD, BUILDING, ICON = keyboard, building, icon 
    
def race():
    num,race = 0,''
    if num == 0:race = 'Amazon'
    elif num == 1:race = 'Atlantean'
    elif num == 2:race = 'Barbarian'
    elif num == 3:race = 'Empire'
    elif num == 4:race = 'Frisian'
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



        

def detect_icon_type(building):
    debug = False
    x_str, y_str = get_mouse_position()
    x, y = int(x_str), int(y_str)
    size = 29
    half = size // 2
    try:
        img = pyautogui.screenshot(region=(x-half, y-half, size, size))
    except:
        return None
    pixels = [p[:3] for p in img.getdata()]
    n = len(pixels)
    r = sum(p[0] for p in pixels) // n
    g = sum(p[1] for p in pixels) // n
    b = sum(p[2] for p in pixels) // n

    # --------------------------------------------------------------
    # 1. GREEN first — they are the brightest and most unique
    # --------------------------------------------------------------
    if g > 85 and r < 65 and b < 20:          # rock-solid green check
        colour = "GREEN"

    # --------------------------------------------------------------
    # 2. Dark orange on dark terrain (the only remaining problem)
    #    → high red, but G very close to R and total brightness low
    # --------------------------------------------------------------
    elif r > 60 and g > 65 and abs(r - g) < 18 and (r + g + b) < 290:
        colour = "ORANGE"

    # --------------------------------------------------------------
    # 3. Everything else → normal distance check (bright icons)
    # --------------------------------------------------------------
    else:
        dg = sqrt((r-36)**2 + (g-104)**2 + (b-3)**2)
        do = sqrt((r-128)**2 + (g-88)**2 + (b-6)**2)
        dr = sqrt((r-98)**2 + (g-52)**2 + (b-8)**2)

        if dg <= 29:
            colour = "GREEN"
        elif do <= 58:
            colour = "ORANGE"
        elif dr <= 48:
            colour = "RED"
        else:
            colour = "none"
    
    if debug:
        short_time = datetime.now().strftime("%H%M%S")
        filename = f"{short_time}_{building}_{colour}.png"
        img.save(os.path.join(WORK_PATH, filename))
        
        print("\nXXX detect_icon_type START XXX")
        print(f"Building Actual Selection: {building}")
        print(f"{short_time}  Actual: {building}   FINAL RESULT: {colour}")
        print("XXX detect_icon_type END XXX\n")        
        _play_sound(colour)
        # ASSUMING F1,F2,F3 (Barbarian) Test is used specificly id the colour
        log_line = f"{datetime.now().strftime('%H%M%S_%f')[:-4]} {x} {y} Actual-{building} Result-{colour}\n"
        debug_save_shm_append(log_line)
    else:
        log_line = f"{datetime.now().strftime('%H%M%S_%f')[:-4]} {x} {y} Building-{building} Result-{colour}\n"
        debug_save_shm_append(log_line)

            
    return colour if colour != "none" else None







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

def _save_snapshot(x=0,y=0,desc='none'):
    if not DEBUG: return
    x_str, y_str = get_mouse_position()
    x, y = int(x_str)+x, int(y_str)+y
    ts = datetime.now().strftime("%H%M%S_%f")[:-4]
    filename = f"{ts}_{desc}_{BUILDING}_{ICON}.png"
    pyautogui.screenshot(region=(x-25, y-25, 50, 50)).save(
        os.path.join(WORK_PATH, filename))



#
#  For Notepad icons example
#
# eg (40,80) = (+40pxls across, +80pxls down)
#
#


def build_item(x=0, y=0):# Current Tab
    stable_click()
    time.sleep(0.05)
    _save_snapshot(0,0,'icon')
    _save_snapshot(x,y,'item')
    stable_click_relative(x, y) 
    unpause_pause(0.15)

def build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg):
    stable_click()
    time.sleep(0.05)
    _save_snapshot(0,0,'icon')
    _save_snapshot(x_tab,y_tab,'tab')
    stable_click_relative(x_tab,y_tab)
    time.sleep(0.05)
    _save_snapshot(x_bldg,y_bldg,'item')
    stable_click_relative(x_bldg, y_bldg)
    unpause_pause(0.15)

    
def build_item_M_S(x_bldg, y_bldg): # Move Medium to Small Tab
    x_tab, y_tab = (-35, 0)
    build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg)
    
def build_item_L_S(x_bldg, y_bldg): # Move Large to Small Tab
    x_tab, y_tab = (-70, 0)
    build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg)

def build_item_L_M(x_bldg, y_bldg): # Move Large to Medium Tab
    x_tab, y_tab = (-35, 0)
    build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg)





    
def err_no_col():
    #print(f"No icon_col, {BUILDING}")
    # uncomment above and comment below if this is Not already done.
    p2autokeym.dbus_send_FM('Widelands','TEXT',{'icon_col':'no colour returned','building type':BUILDING})



    
def in_building_dialog(x,y):# For Dismantles & Upgrades
    ctrl_press()#ctrl_on()
    stable_click()   
    _save_snapshot(0,0,'icon')
    time.sleep(0.05)
    _save_snapshot(x,y,BUILDING)
    stable_click_relative(x, y) 
    time.sleep(0.05)
    ctrl_release()#ctrl_off()
    unpause_pause()


def unpause_pause(delay=0.2):
    KEYBOARD.send_keys("<pause>")
    time.sleep(delay)
    KEYBOARD.send_keys("<pause>")


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
        #print(f"Missing {func_name}")
        # uncomment above and comment below if this is Not already done.
        p2autokeym.dbus_send_FM('Widelands','TEXT',{'Error': f"Missing {func_name}"})





# Amazon
# ===============================================
# Amazon — FUNCTIONS (F1–F12 + end + hyphen + equal + backslash + rightbracket)
# ===============================================


def Amazon_F1(keyboard):
    btype = 'Stonecutter'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (10, 45)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Amazon_F2(keyboard):
    btype = 'Woodcutter'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    if toggle_tab:  # remove worker
        Amazon_remove_worker(70, -40)
    else: # Build Site
        item_pos = (60, 45) 
        if icon_col == 'RED':
            build_item(*item_pos)
        elif icon_col == 'ORANGE':
            build_item_M_S(*item_pos)
        elif icon_col == 'GREEN':
            build_item_L_S(*item_pos)
        else:
            err_no_col()

def Amazon_F3(keyboard):
    btype = 'Jungle_Preserve'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    if toggle_tab:  # remove worker
        Amazon_remove_worker(70, -40)
    else: # Build Site
        item_pos = (105, 45)
        if icon_col == 'RED':
            build_item(*item_pos)
        elif icon_col == 'ORANGE':
            build_item_M_S(*item_pos)
        elif icon_col == 'GREEN':
            build_item_L_S(*item_pos)
        else:
            err_no_col()

def Amazon_F4(keyboard):
    btype = 'Water_Gatherer'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (5, 95)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Amazon_F5(keyboard):
    btype = 'Cassava_Root_Cooker'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (75, 95)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_M(*item_pos)  # GREEN → medium tab
    else:
        err_no_col()

def Amazon_F6(keyboard):
    btype = 'Chocolate_Brewery'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (105, 95)  # corrected from 125 → 95 to match actual position
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_M(*item_pos)
    else:
        err_no_col()

def Amazon_F7(keyboard):
    btype = 'Charcoal_Kiln'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    if toggle_tab:# infinate Production of charcoal
        start_pos = capture_mouse_pos()
        in_building_dialog(-175, 20)
        stable_click(3)  # right-click
        restore_mouse_pos(start_pos)

    else:#'Charcoal_Kiln'
        item_pos = (25, 95)
        if icon_col == 'ORANGE':
            build_item(*item_pos)
        elif icon_col == 'GREEN':
            build_item_L_M(*item_pos)
        else:
            err_no_col()

def Amazon_F8(keyboard):
    btype = 'Food_Preserver'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (175, 95)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_M(*item_pos)
    else:
        err_no_col()

def Amazon_F9(keyboard):
    btype = 'DressMakery'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (-25, 95)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_M(*item_pos)
    else:
        err_no_col()

def Amazon_F10(keyboard):
    btype = 'Rare_Tree_Plantation'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    if toggle_tab:  #  Infinate Rare Tree Production
        start_pos = capture_mouse_pos()
        in_building_dialog(-285, 0) 
        stable_click(3)
        unpause_pause(0.02)
        restore_mouse_pos(start_pos)
    else: #  # Build Site
        item_pos = (125, 50)
        if icon_col == 'ORANGE':
            build_item(*item_pos)
        elif icon_col == 'GREEN':
            build_item_L_M(*item_pos)
        else:
            err_no_col()

def Amazon_F11(keyboard):
    btype = 'Hunter_Gatherer'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (160, 45)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Amazon_F12(keyboard):
    btype = 'Wilderness_Keeper'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (60, 85)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()


def Amazon_end(keyboard):
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    btype = 'Furnace' if toggle_tab else 'Stone_Workshop'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)

    # Toggle changes only the item position
    item_pos = (75, 50) if toggle_tab else (175, 45)

    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_M(*item_pos)
    else:
        err_no_col()

def Amazon_plus(keyboard):
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    btype = 'Rope_Weaver' if toggle_tab else 'Liana_Cutter'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)

    # Toggle changes only the item position
    item_pos = (25, 45) if toggle_tab else (205, 45)
    if toggle_tab:#'Rope_Weaver'
        if icon_col == 'ORANGE':
            build_item(*item_pos)
        elif icon_col == 'GREEN':
            build_item_L_M(*item_pos)
        else:
            err_no_col()
    else:#'Liana_Cutter'
        if icon_col == 'RED':
            build_item(*item_pos)
        elif icon_col == 'ORANGE':
            build_item_M_S(*item_pos)
        elif icon_col == 'GREEN':
            build_item_L_S(*item_pos)
        else:
            err_no_col()

def Amazon_equal(keyboard):
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    btype = 'Warriors_Dwelling' if toggle_tab else 'Tower'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)

    # Toggle changes only the item position
    #      'Warriors_Dwelling'     else     'Tower' (default)
    item_pos = (125, 145) if toggle_tab else (175, 145)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_M(*item_pos)
    else:
        err_no_col()

def Amazon_hyphen(keyboard):
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    
    if toggle_tab:  # Upgrade_to_Rare — special case (dismantle + right-click)
        _set_io(keyboard, 'Upgrade_to_Rare', 'none')
        start_pos = capture_mouse_pos()
        in_building_dialog(-210, 0)
        stable_click(3)  # right-click
        restore_mouse_pos(start_pos)
    else:  # Patrol_Post — normal build
        btype = 'Patrol-Post'
        icon_col = detect_icon_type(btype)
        _set_io(keyboard, btype, icon_col)
        item_pos = (160, 100)

        if icon_col == 'RED':
            build_item(*item_pos)
        elif icon_col == 'ORANGE':
            build_item_M_S(*item_pos)
        elif icon_col == 'GREEN':
            build_item_L_S(*item_pos)
        else:
            err_no_col()






def Amazon_scroll_lock(keyboard):
    _set_io(keyboard, 'Amazon_scroll_lock', 'none')
    in_building_dialog(-165, 0) # Dismantle Woodcutter

    
def Amazon_backslash(keyboard):
    # Dismantle Guardhouse, Tower, Castle
    _set_io(keyboard, 'Amazon_backslash', 'none')
    in_building_dialog(-130, 0)

    
def Amazon_rightbracket(keyboard):
    # Dismantle  Quarry
    _set_io(keyboard, 'Amazon_rightbracket', 'none')
    in_building_dialog(-235, 0)

def Amazon_leftbracket(keyboard):
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    _set_io(keyboard, 'Amazon_leftbracket', 'none')
    if toggle_tab:  # 
        pass
    else:
        # Double Click
        stable_click()
        time.sleep(0.1)
        stable_click()
        unpause_pause(0.1)

def Amazon_remove_worker(x,y):
    start_pos = capture_mouse_pos()
    in_building_dialog(70, -40)
    unpause_pause(0.1)
    stable_click(3)
    restore_mouse_pos(start_pos)


# Atlantean

# ===============================================
# Atlantean FUNCTIONS (F1–F12 + end + hyphen + equal + backslash + rightbracket)
# ===============================================

def Atlantean_F1(keyboard):
    btype = 'Quarry'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (5, 40)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F2(keyboard):
    btype = 'Woodcutter'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (60, 45)  # standardised Y to match most buildings
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F3(keyboard):
    btype = 'Forester'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (105, 45)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F4(keyboard):
    btype = 'Well'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (55, 95)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F5(keyboard):
    btype = 'Bakery'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (175, 50)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F6(keyboard):
    btype = 'Smokery'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (75, 50)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F7(keyboard):
    btype = 'Mill'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (125, 50)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F8(keyboard):
    btype = 'Smelter'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (20, 95)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F9(keyboard):
    btype = 'Weaponsmith'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (125, 95)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F10(keyboard):
    btype = 'Armoursmith'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (175, 95)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F11(keyboard):
    btype = 'Fish'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (155, 45)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_F12(keyboard):
    btype = 'Fishbreader'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (205, 45)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_end(keyboard):
    btype = 'SawMill'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (25, 50)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Atlantean_hyphen(keyboard):
    btype = 'Guardhouse'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (200, 100)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Atlantean_equal(keyboard):
    btype = 'Tower'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (125, 135)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
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
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (5, 40)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F2(keyboard):
    btype = 'Woodcutter'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (60, 45)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F3(keyboard):
    btype = 'Forester'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (105, 45)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F4(keyboard):
    btype = 'Well'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (55, 95)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F5(keyboard):
    btype = 'Bakery'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (175, 50)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F6(keyboard):
    btype = 'Smokery'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (75, 50)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F7(keyboard):
    btype = 'Mill'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (125, 50)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F8(keyboard):
    btype = 'Smelter'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (20, 95)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F9(keyboard):
    btype = 'Weaponsmith'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (125, 95)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F10(keyboard):
    btype = 'Armoursmith'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (175, 95)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F11(keyboard):
    btype = 'Fish'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (155, 45)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_F12(keyboard):
    btype = 'Fishbreader'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (205, 45)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_end(keyboard):
    btype = 'SawMill'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (25, 50)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
        build_item_M_S(*item_pos)
    else:
        err_no_col()

def Barbarian_hyphen(keyboard):
    btype = 'Guardhouse'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (200, 100)
    if icon_col == 'RED':
        build_item(*item_pos)
    elif icon_col == 'ORANGE':
        build_item_M_S(*item_pos)
    elif icon_col == 'GREEN':
        build_item_L_S(*item_pos)
    else:
        err_no_col()

def Barbarian_equal(keyboard):
    btype = 'Tower'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    item_pos = (125, 135)
    if icon_col == 'ORANGE':
        build_item(*item_pos)
    elif icon_col == 'GREEN':
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
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(5, 40)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, -25, 40)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, -60, 40)
    else:
        err_no_col()

def Empire_F2(keyboard):
    btype = 'Woodcutter'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(60, 40)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 20, 55)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, -10, 45)
    else:
        err_no_col()

def Empire_F3(keyboard):
    btype = 'Forester'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(105, 45)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 80, 45)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, 40, 45)
    else:
        err_no_col()

def Empire_F4(keyboard):
    btype = 'Well'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(55, 95)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 25, 95)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, -15, 95)
    else:
        err_no_col()

def Empire_F5(keyboard):
    btype = 'Bakery'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(175, 50)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, 140, 50)
    else:
        err_no_col()

def Empire_F6(keyboard):
    btype = 'Smokery'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(75, 50)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, 40, 50)
    else:
        err_no_col()

def Empire_F7(keyboard):
    btype = 'Mill'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(125, 50)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, 95, 50)
    else:
        err_no_col()

def Empire_F8(keyboard):
    btype = 'Smelter'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(20, 95)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, -15, 95)
    else:
        err_no_col()

def Empire_F9(keyboard):
    btype = 'Weaponsmith'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(125, 95)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, 95, 95)
    else:
        err_no_col()

def Empire_F10(keyboard):
    btype = 'Armoursmith'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(175, 95)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, 140, 95)
    else:
        err_no_col()

def Empire_F11(keyboard):
    btype = 'Fish'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(155, 45)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 120, 45)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, 85, 45)
    else:
        err_no_col()

def Empire_F12(keyboard):
    btype = 'Fishbreader'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(205, 45)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 170, 45)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, 140, 45)
    else:
        err_no_col()

def Empire_end(keyboard):
    btype = 'SawMill'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(25, 50)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, -15, 50)
    else:
        err_no_col()

def Empire_hyphen(keyboard):
    btype = 'Guardhouse'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(200, 100)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 170, 100)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, 140, 100)
    else:
        err_no_col()

def Empire_equal(keyboard):
    btype = 'Tower'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(125, 135)
    elif icon_col == 'GREEN':
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
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(5, 40)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, -25, 40)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, -60, 40)
    else:
        err_no_col()

def Frisian_F2(keyboard):
    btype = 'Woodcutter'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(60, 40)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 20, 55)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, -10, 45)
    else:
        err_no_col()

def Frisian_F3(keyboard):
    btype = 'Forester'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(105, 45)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 80, 45)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, 40, 45)
    else:
        err_no_col()

def Frisian_F4(keyboard):
    btype = 'Well'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(55, 95)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 25, 95)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, -15, 95)
    else:
        err_no_col()

def Frisian_F5(keyboard):
    btype = 'Bakery'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(175, 50)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, 140, 50)
    else:
        err_no_col()

def Frisian_F6(keyboard):
    btype = 'Smokery'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(75, 50)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, 40, 50)
    else:
        err_no_col()

def Frisian_F7(keyboard):
    btype = 'Mill'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(125, 50)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, 95, 50)
    else:
        err_no_col()

def Frisian_F8(keyboard):
    btype = 'Smelter'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(20, 95)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, -15, 95)
    else:
        err_no_col()

def Frisian_F9(keyboard):
    btype = 'Weaponsmith'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(125, 95)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, 95, 95)
    else:
        err_no_col()

def Frisian_F10(keyboard):
    btype = 'Armoursmith'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(175, 95)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, 140, 95)
    else:
        err_no_col()

def Frisian_F11(keyboard):
    btype = 'Fish'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(155, 45)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 120, 45)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, 85, 45)
    else:
        err_no_col()

def Frisian_F12(keyboard):
    btype = 'Fishbreader'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(205, 45)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 170, 45)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, 140, 45)
    else:
        err_no_col()

def Frisian_end(keyboard):
    btype = 'SawMill'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(25, 50)
    elif icon_col == 'GREEN':
        notepd_tab_select(-35, 0, -15, 50)
    else:
        err_no_col()

def Frisian_hyphen(keyboard):
    btype = 'Guardhouse'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'RED':
        notepd_strait(200, 100)
    elif icon_col == 'ORANGE':
        notepd_tab_select(-35, 0, 170, 100)
    elif icon_col == 'GREEN':
        notepd_tab_select(-65, 0, 140, 100)
    else:
        err_no_col()

def Frisian_equal(keyboard):
    btype = 'Tower'
    icon_col = detect_icon_type(btype)
    _set_io(keyboard, btype, icon_col)
    if icon_col == 'ORANGE':
        notepd_strait(125, 135)
    elif icon_col == 'GREEN':
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
 
    
