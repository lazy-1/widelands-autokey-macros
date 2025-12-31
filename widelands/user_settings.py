# widelands/current_tribe.py
# ────────────────────────────────────────────────────────────────
#   0 = Amazon
#   1 = Atlantean
#   2 = Barbarian
#   3 = Empire
#   4 = Frisian
# ────────────────────────────────────────────────────────────────
# In
# load_USR_defaults() find
# 
# USR['race_number'] =
#
# Set it to the Tribe Number You are playing This is Critical!!!
#
# ────────────────────────────────────────────────────────────────
#   You don't need to touch anything below this line
# ────────────────────────────────────────────────────────────────
import os
from .sharedic import USR

_MAPPING = {
    0: 'Amazon',
    1: 'Atlantean',
    2: 'Barbarian',
    3: 'Empire',
    4: 'Frisian',
}

def get_tribe():
    load_USR_defaults()
    num = USR['race_number']
    tribe = _MAPPING.get(num, 'Atlantean')  # safe fallback
    USR['tribe'] = tribe
    return tribe



def load_USR_defaults():
    """
    Loads all user-adjustable defaults directly into USR.
    Edit the values below — this is the only place you need to change things.
    Each setting has a simple explanation of what it does and how it affects the macros.
    """
    global USR

    # ────────────────────────────────────────────────────────────────
    # Race & Basic Setup
    # ────────────────────────────────────────────────────────────────
    # Which race you are currently playing
    # (0=Amazon, 1=Atlantean, 2=Barbarian, 3=Empire, 4=Frisian)

    USR['race_number'] = 0          # Change this number to match your game



    # ────────────────────────────────────────────────────────────────
    # Where debug log and snapshots are saved
    #
    # As well as the core road create transient variable, this literally
    # has thousands of read writes, not good for ssd systems
    # hence the use of /dev/shm (Ram disk) 
    #
    # ────────────────────────────────────────────────────────────────
    # (RAM disk '/dev/shm' is fastest, auto-deletes on reboot)
    # This MUST be a valid constructible path. i.e. /dev/shm/ is available
    # Widelands directory will be created via os.mkdir
    # without this build roads can not work.
    
    USR['work_path'] = '/dev/shm/Widelands/'
    
    # leave this here to check/create work_path or comment out and disable
    # road building and any debugging.
    
    if not os.path.exists(USR['work_path']):
        os.mkdir(USR['work_path'])
    # Path to the transient file for road building, must be in work_path
    
    USR['transient_path'] = USR['work_path']+'autokey_transient_store.json'






    
    # ────────────────────────────────────────────────────────────────
    # Audio Feedback
    # ────────────────────────────────────────────────────────────────
    # Where your sound files are stored (bell.oga, complete.oga, etc.)
    # Change to your real path
    #  example USR['sound_dir'] = '/home/yourusername/Sounds/notifications/'

    # This is My personal path to the sounds. So edit it!
    
    USR['sound_dir'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'Sounds', 'Application', 'Notification')) + '/'

    # Turn all sounds on/off (pause-unpause beeps, error tones, etc.)
    
    USR['enable_sounds'] = True 





    # ────────────────────────────────────────────────────────────────
    # Dictionary of sound files for different results/events
    # ────────────────────────────────────────────────────────────────
    # Key = event type (e.g. 'red', 'big_error'),
    # Value = filename (.oga recommended)
    # Leave value as '' to disable a sound

    USR['sound_files'] = {
    'red': 'bell.oga',                  # Build site: large/red Not Used
    'orange': 'complete.oga',           # Build site: medium/orange Not Used
    'green': 'dialog-warning.oga',      # Build site: small/green Not Used
    'big_error': 'phone-incoming-call.oga',  # Major error/alert
    'meedmeep': 'MeebMeeb.ogg',         # reload module feedback
    'down1': 'KDE_Window_Close.ogg',    # Downward tone Not Used
    'up1': 'KDE_Window_Open.ogg',       # Upward tone Not Used
    'down2': 'Chatdown.ogg',            # Downward tone
    'up2': 'Chatup.ogg',                # Upward tone
    'down3': 'Musica Restore Down.ogg', # Downward tone Not Used
    'up3': 'Musica Restore Up.ogg',     # Upward tone Not Used
    'sharpstrum1': 'sharp_organ.ogg',   # Sharp alert
    # Add your own here, e.g.:
    # 'custom_success': 'success.oga',
    }



    

    
    # ────────────────────────────────────────────────────────────────
    # Pause enable and pause delay.
    # unpause_pause(delay=USR['pause_delay']):
    # ────────────────────────────────────────────────────────────────
    # If the delay is too short the pause is not registered.
    
    USR['enable_pause'] = True
    USR['pause_delay'] = 0.2
    


    

    # ────────────────────────────────────────────────────────────────
    # Debug & Logging all Use USR['work_path']
    # ────────────────────────────────────────────────────────────────
    # Full debug mode: saves screenshots + lots of log lines (makes macros slower)
    # Turn True only when tuning or finding bugs

    USR['debug'] = False
    
    # Separate log file for debug messages (debug_save_shm_append)
    # Set False to completely disable the text log file
    
    USR['log_enabled'] = True       

    





    
    # ────────────────────────────────────────────────────────────────
    # stable_click(button=1):
    # ────────────────────────────────────────────────────────────────

    # Delay after cursor warp (stabilizes position before click)
    # Gives the X server a brief moment to fully process the warp_pointer() 
    # so Widelands doesn't see an old/inconsistent cursor
    # position during dialog placement.
    # Too short = dialog may open offset or misaligned
    # Too long = feels slightly sluggish
    # Typical range: 0.03–0.08 (0.04 is a safe middle ground)

    USR['delay_stable_settle'] = 0.04   

    # Short hold time during the click itself (press → release)
    # Mimics a real human finger press duration so
    # the game reliably detects the button event.
    # Too short = some SDL2 games ignore the click (instant press/release looks like noise)
    # Too long = click feels noticeably delayed
    # Typical range: 0.01–0.05 (0.02 is very reliable and barely perceptible)

    USR['delay_click_hold'] = 0.02      





    
    # ────────────────────────────────────────────────────────────────
    # stable_click_relative(dx=0, dy=0, button=1):
    # ────────────────────────────────────────────────────────────────

    # Small settle — gives X server time to register the cursor warp before click

    USR['warp_settle'] = 0.05

    # Short realistic hold —
    # mimics human finger press so the game detects the click properly

    USR['click_hold'] = 0.03






    
    # ────────────────────────────────────────────────────────────────
    # ctrl_press()
    # ────────────────────────────────────────────────────────────────

    # Short sleep after pressing the ctrl key so that it is registered
    # Race conditions apply here if you want ctrl held then this needs to
    # be realistic.
    
    USR['ctrl_press_delay'] = 0.05





    
    # ────────────────────────────────────────────────────────────────
    # Build_Zigzag_Road(keyboard):
    # ────────────────────────────────────────────────────────────────

    # Wait for dialog to open and settle (tune 0.05–0.22)
    
    USR['wait_for_dialog1'] = 0.05




    

    # ────────────────────────────────────────────────────────────────
    # Build_Connect_Road(keyboard):
    # ────────────────────────────────────────────────────────────────

    # Wait for stable click to register before it proceeds to ctrl_release

    USR['wait1'] = 0.1

    # A wait for Dialog to open properly.

    USR['wait_for_dialog2'] = 0.1



    

    # ────────────────────────────────────────────────────────────────
    # Build_New_Road(keyboard):
    # ────────────────────────────────────────────────────────────────

    # These are waits when building a new road.
    # Wait to make sure the game registers the mouse click

    USR['wait_to_register1'] = 0.1

    # Wait for the dialog to fully render

    USR['wait_for_dialog3'] = 0.1

    # Wait for the click on dialog to fully register before ctrl release
    # reuse this in else: if you have issues and want separate go for it.

    USR['wait_to_register2'] = 0.05
    


    

    # ────────────────────────────────────────────────────────────────
    # in_building_dialog(x,y):
    # build_item(x=0, y=0):
    # build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg):
    # ────────────────────────────────────────────────────────────────

    # The get_screenshot_info has a quirk. A race condition between it and
    # the wideland responses, ironically the snapshot needs to be throttled.
    
    USR['wait_screenshot'] = 0.05
    
    # Common wait for Dialog clicks to be registered by the game before Proceeding

    USR['wait_to_register3'] = 0.05















