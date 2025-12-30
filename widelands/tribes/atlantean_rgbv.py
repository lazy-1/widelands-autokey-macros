# shell for rgb and variance filtering of image
#
#
# tribe_rgbv.py (eg amazon_rgbv.py)
# ────────────────────────────────────────────────────────────────
#  Tribe-specific RGB + variance classifiers
#
#  Purpose:
#    These functions classify dialog icons using the
#    average RGB values and pixel variance from the screenshots.
#    Each tribe has its own file because
#    colors/icons start points differ in dialogs.
#
#  How it works:
#    Functions receive four arguments:
#      r, g, b     → average color of the screenshot area
#      variance    → how much the pixels differ from the average
#
#    Return tuple: (is_buildable: bool, site_name: str)
#      - True + tab color ('red'/'orange'/'green'/'blue') = buildable
#            This is already defined in common.py module id_site_tab_color()
#
#      - False + icon name ('upgrade_tower', 'garrison', etc.) = non-buildable
#
#  How to create / edit / tune:
#    1. Set DEBUG = True in common.py
#    2. Hover mouse over the site you want to detect
#    3. Press the shortcut key that triggers the action/screenshot
#    4. Look in the temp directory (usually /dev/shm/Widelands/) user defined
#       Example filename:
#              165043_61_unknown-F-(39, 50, 36, 4054)-4054_RGB039_050_036.png
#       Breakdown:
#         - 165043_61          → timestamp
#         - unknown            → description if unknown you'll know
#         - T/F                → True/False (buildable or not)
#                                   F so it is a building you clicked on
#                                   T it is a build site (red green or orange)
#         - (39, 50, 36, 4054) → detected colour of the snapshot
#         - 4054               → variance
#         - RGB039_050_036     → r=39, g=50, b=36
#
#    5. Use the filename to get real r,g,b,variance values
#       - Write a tolerance check: abs(r - 39) <= 5
#       - Add variance range: e.g. 3000 < variance < 5000
#       - Test different states (buildable, upgrade, garrison, etc.)
#       - Adjust tolerances: wider (±8–12) for noisy images, tighter (±3–5) for clean ones
#
#    6. Return the correct tuple:
#       - Buildable tab → (True, 'red'), (True, 'orange'), (True, 'green'), (True, 'blue') Already defined and local to the common.py
#       - Non-buildable → (False, 'upgrade_tower'), (False, 'garrison'), (False, 'swirl'), etc.
#         This is where you come in, defining what the image is associated with.
#
#  Tips:
#    - Variance is usually higher for colorful/complex icons, lower for flat/empty areas
#    - Add comments with the RGB/variance range you matched
#    - If detection is flaky, take multiple screenshots of the same state
#      and look for the tightest common range
#
#  Add new tribes:
#    Create new_tribe_rgbv.py with the same two functions:
#        id_building_via_dialog_tells, id_dialog_icon
#
#  sample functions provided..
# ────────────────────────────────────────────────────────────────


def id_dialog_icon(r, g, b, variance):
    if (abs(r - 97) <= 5 and abs(g - 81) <= 5 and abs(b - 54) <= 5
        and 1000 < variance < 2000):
        return (False, 'upgrade_tower')
    
    if (abs(r - 104) <= 10 and abs(g - 83) <= 5 and abs(b - 51) <= 10
        and 1800 < variance < 2500):# Charcoal Kiln wares indicator..
        return (False, 'Charcoal_kiln')


    return (False, f"({r}, {g}, {b}, {int(variance)})")

    
def id_building_via_dialog_tells(r, g, b, variance):
    if (abs(r - 118) <= 10 and abs(g - 106) <= 10 and abs(b - 26) <= 10
        and 10000 < variance < 12500):# 'Gar' image
        return (False, 'Garrison')
        
    if (abs(r - 88) <= 3 and abs(g - 68) <= 3 and abs(b - 40) <= 3
        and 250 < variance < 500):# Blank brown image
        return (False, 'Standard_brown')

    if (abs(r - 87) <= 5 and abs(g - 68) <= 5 and abs(b - 37) <= 5
        and 6000 < variance < 7000):# Tiny Woodcutter icon
        return (False, 'Woodcutter')
        
    if (abs(r - 75) <= 5 and abs(g - 66) <= 5 and abs(b - 36) <= 5
        and 6000 < variance < 7000):# Tiny Forester icon
        return (False, 'Forester')

    if (abs(r - 83) <= 5 and abs(g - 69) <= 5 and abs(b - 46) <= 5
        and 7500 < variance < 8500):# Tiny Quary icon
        return (False, 'Quary')

    if (abs(r - 76) <= 5 and abs(g - 63) <= 5 and abs(b - 41) <= 3
        and 5250 < variance < 5600):# Tiny Fishbreeder icon
        return (False, 'Fishbreeder')
        
    if (abs(r - 75) <= 5 and abs(g - 61) <= 5 and abs(b - 37) <= 3
        and 5000 < variance < 5400):# Tiny Fish icon
        return (False, 'Fish')

    if (abs(r - 76) <= 5 and abs(g - 58) <= 5 and abs(b - 32) <= 3
        and 3500 < variance < 4400):# Tiny Well icon
        return (False, 'Well')

    if (abs(r - 108) <= 10 and abs(g - 76) <= 5 and abs(b - 42) <= 10
        and 3000 < variance < 5000):#  Scout arrow near fish...
        return (False, 'Scout')
    
    return (False, f"({r}, {g}, {b}, {int(variance)})") 
