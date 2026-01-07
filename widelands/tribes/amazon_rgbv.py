
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
    if (abs(r - 107) <= 5 and abs(g - 76) <= 5 and abs(b - 48) <= 5
        and variance < 11000):
        return (False, 'swirl')
    if (abs(r - 113) <= 5 and abs(g - 84) <= 5 and abs(b - 45) <= 5
        and variance < 3500):
        return (False, 'Charcoal_Kiln')
    
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

    return (False, f"({r}, {g}, {b}, {int(variance)})") 

def id_building_via_dialog_tells(r, g, b, variance):
    if (abs(r - 124) <= 12 and abs(g - 106) <= 10 and abs(b - 26) <= 10
        and 10000 < variance < 12500):# 'Gar' image
        return (False, 'Garrison')
    
    if (abs(r - 88) <= 3 and abs(g - 68) <= 3 and abs(b - 40) <= 3
        and 250 < variance < 500):# Blank brown image
        return (False, 'Standard_brown')
        
    if (abs(r - 96) <= 3 and abs(g - 76) <= 3 and abs(b - 45) <= 3
        and 250 < variance < 450):#Blank brown image Woodcutter is building dialog
        return (False, 'Lighter_brown')
        
    if (abs(r - 66) <= 3 and abs(g - 52) <= 5 and abs(b - 27) <= 5
        and 1800 < variance < 2500):# Tiny Liana icon
        return (False, 'Liana')

    if (abs(r - 70) <= 5 and abs(g - 58) <= 5 and abs(b - 40) <= 5
        and 3000 < variance < 4000):# Tiny StoneCutter icon
        return (False, 'Stonecutter')


    if (abs(r - 58) <= 5 and abs(g - 63) <= 5 and abs(b - 24) <= 5
        and 2500 < variance < 3200):# Tiny Jungle Preserver
        return (False, 'Jungle_Preserver')

    if (abs(r - 64) <= 5 and abs(g - 67) <= 5 and abs(b - 33) <= 5
        and 3000 < variance < 4000):# Tiny Jungle Preserver Master
        return (False, 'Jungle_PreserverM')


    
    if (abs(r - 105) <= 5 and abs(g - 81) <= 5 and abs(b - 56) <= 5
        and 9000 < variance < 11500):# Tiny Woodcutter icon Master!
        return (False, 'WoodcutterM')

    if (abs(r - 71) <= 3 and abs(g - 52) <= 5 and abs(b - 27) <= 5
        and 1800 < variance < 2500):# Tiny Woodcutter icon
        return (False, 'Woodcutter')
    
    return (False, f"({r}, {g}, {b}, {int(variance)})")  
    
