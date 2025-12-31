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
    # Which race you are currently playing (0=Amazon, 1=Atlantean, 2=Barbarian, 3=Empire, 4=Frisian)

    USR['race_number'] = 1          # Change this number to match your game

    # ────────────────────────────────────────────────────────────────
    # def stable_click(button=1):
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




    
    # Delay after stable_click (time for dialog to open before snapshot)
    # Increase if dialog not ready, decrease if too slow
    
    USR['delay_click'] = 0.2          

    # Short hold time during click (press → release)
    USR['delay_hold'] = 0.03          # Small but realistic click duration

    # Delay after right-click close (before restoring mouse position)
    USR['delay_close'] = 0.12         # Prevents warp during dialog close animation

    # Delay after pause-unpause (feedback & mode clear)
    USR['pause_delay'] = 0.15         # Main feedback delay, adjust for feel


    # ────────────────────────────────────────────────────────────────
    # Audio & Visual Feedback
    # ────────────────────────────────────────────────────────────────
    # Enable unpause_pause function
    USR['enable_pause'] = True
    
    # Turn all sounds on/off (pause-unpause beeps, error tones, etc.)
    USR['enable_sounds'] = True     # Set False if you don't want any sound feedback

    # Where your sound files are stored (bell.oga, complete.oga, etc.)
    USR['sound_dir'] = '/home/yourusername/Sounds/notifications/'  # Change to your real path

    # ────────────────────────────────────────────────────────────────
    # Debug & Logging
    # ────────────────────────────────────────────────────────────────
    # Full debug mode: saves screenshots + lots of log lines (makes macros slower)
    USR['debug'] = False            # Turn True only when tuning or finding bugs

    # Separate log file for debug messages (debug_save_shm_append)
    USR['log_enabled'] = True       # Set False to completely disable the text log file

    # Where debug log and snapshots are saved (RAM disk is fastest, auto-deletes on reboot)
    USR['work_path'] = '/dev/shm/Widelands/'  # Change if you don't want RAM disk

    # ────────────────────────────────────────────────────────────────
    # Screenshot & Detection (advanced tuning)
    # ────────────────────────────────────────────────────────────────
    # Size of screenshot area for dialog detection (width, height in pixels)
    USR['shot_size'] = (41, 29)     # Wider = more stable detection, but slightly slower

    # Add your own settings below this line
    # USR['my_custom_key'] = 'F13'
    # USR['enable_extra_check'] = True











