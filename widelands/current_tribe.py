# widelands/current_tribe.py
# ────────────────────────────────────────────────────────────────
#   Edit ONLY the number below to change your current tribe.
#   0 = Amazon
#   1 = Atlantean
#   2 = Barbarian
#   3 = Empire
#   4 = Frisian
# ────────────────────────────────────────────────────────────────

CURRENT_TRIBE_NUMBER = 0          # ← change this number ←

# ────────────────────────────────────────────────────────────────
#   You don't need to touch anything below this line
# ────────────────────────────────────────────────────────────────


_MAPPING = {
    0: 'Amazon',
    1: 'Atlantean',
    2: 'Barbarian',
    3: 'Empire',
    4: 'Frisian',
}

def get_tribe():
    num = CURRENT_TRIBE_NUMBER
    tribe = _MAPPING.get(num, 'Atlantean')  # safe fallback
    from widelands.core import CONTEXT
    CONTEXT['tribe'] = tribe
    return tribe

