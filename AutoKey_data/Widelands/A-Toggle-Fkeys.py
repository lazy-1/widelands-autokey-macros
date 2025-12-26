# Will I use it? , objective, giving a 2nd set of F keys
# so instead of 12, you have 24
# Sound feedback, Down = normal, Up = Second Set
#
# The Functions Associated with 'Up' need to access
#   transient_store_get in order to get state
#  True == UP , False == Down(default)

#key = # tab

import widelands

do = widelands.transient_store_get('widelands_Toggle_Fkeys',False)

if do:
    widelands.transient_store_set('widelands_Toggle_Fkeys',False)
    widelands._play_sound('down2')
else:
    widelands.transient_store_set('widelands_Toggle_Fkeys',True)
    widelands._play_sound('up2')
 




