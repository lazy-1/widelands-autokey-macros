# shell for rgb and variance filtering of image
#
#
# tribe_rgbv.py
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
#       Example filename: 145411_35_Stonecutter-T-green-4164_RGB018_087_008.png
#       Breakdown:
#         - 145411_35_     → timestamp
#         - Stonecutter    → description if undef you get raw rgb and variant
#         - T/F            → True/False (buildable or not) T so it is a build site
#         - green          → detected site/tab
#         - 4164           → variance
#         - RGB018_087_008 → r=18, g=87, b=8
#
#    5. Use the filename to get real r,g,b,variance values
#       - Write a tolerance check: abs(r - 18) <= 5
#       - Add variance range: e.g. 3000 < variance < 5000
#       - Test different states (buildable, upgrade, garrison, etc.)
#       - Adjust tolerances: wider (±8–12) for noisy images, tighter (±3–5) for clean ones
#
#    6. Return the correct tuple:
#       - Buildable tab → (True, 'red'), (True, 'orange'), (True, 'green'), (True, 'blue')
#       - Non-buildable → (False, 'upgrade_tower'), (False, 'garrison'), (False, 'swirl'), etc.
#
#  Tips:
#    - Variance is usually higher for colorful/complex icons, lower for flat/empty areas
#    - Add comments with the RGB/variance range you matched
#    - Keep return strings consistent with _set_io() / build_item logic
#    - If detection is flaky, take multiple screenshots of the same state
#      and look for the tightest common range
#
#  Add new tribes:
#    Create new_tribe_rgbv.py with the same three functions:
#      id_site_tab_color, id_building_via_dialog_tells, id_dialog_icon
# ────────────────────────────────────────────────────────────────





def id_dialog_icon(r, g, b, variance):
    return (False, f"({r}, {g}, {b}, {int(variance)})")

def id_building_via_dialog_tells(r, g, b, variance):
    return (False, f"({r}, {g}, {b}, {int(variance)})")




