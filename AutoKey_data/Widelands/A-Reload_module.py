# For Development, used to reload module after edit.
#key = # `

import importlib
import sys
# Force reload widelands module on every run 
# — perfect for live development
if 'widelands' in sys.modules:
    importlib.reload(sys.modules['widelands'])
    widelands = sys.modules['widelands']   
    print("widelands module RELOADED")
else:
    import widelands
    print("widelands module freshly imported")

widelands._play_sound('meedmeep')
print("Reset transient_store variables to False")
widelands.transient_store_set('widelands_zigzag_rd',False)
widelands.transient_store_set('widelands_join_rd',False)
widelands.transient_store_set('widelands_long_rd',False)







