from ..sharedic import USR, update_USR
from ..common import *

# Amazon
# ===============================================
# Amazon — FUNCTIONS (F1–F12 + end + hyphen + equal + backslash + rightbracket)
# ===============================================


    
def F1():
    btype = 'Stonecutter'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    item_pos = (10, 50)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error('frog nuckles')

def F2():
    btype = 'Woodcutter'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
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

    
    _, built, var = get_screenshot_info(x=0,y=-90,desc='detect_dialog',area=(15,15))

    if site == 'swirl':
        if built == 'building_built':#, 'remove_worker'
            in_building_dialog(68, -34)
            return
            
  
    output_error(f'{built} toggled-{toggle_tab}')


def F3():
    btype = 'Jungle_Preserve'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    if build:
        item_pos = (105, 45)
        if site == 'red':
            build_item(*item_pos)
        elif site == 'orange':
            build_item_M_S(*item_pos)
        elif site == 'green':
            build_item_L_S(*item_pos)
        else:
            output_error()
        return
    _, built, var = get_screenshot_info(x=0,y=-90,desc='detect_dialog',area=(15,15))
    if site == 'swirl': # remove worker
        
        in_building_dialog(68, -34, 'remove_worker')
        
    


def F4():
    btype = 'Water_Gatherer'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    item_pos = (10, 95)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error()

def F5():
    btype = 'Cassava_Root_Cooker'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    item_pos = (75, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)  # GREEN → medium tab
    else:
        output_error()

def F6():
    btype = 'Chocolate_Brewery'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    item_pos = (125, 95)  # corrected from 125 → 95 to match actual position
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)
    else:
        output_error()

def F7():
    btype = 'Charcoal_Kiln'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    if build:
        item_pos = (25, 95)
        if site == 'orange':
            build_item(*item_pos)
        elif site == 'green':
            build_item_L_M(*item_pos)
        else:
            output_error()
    if site == 'Charcoal_Kiln':
        in_building_dialog(-174, 20)
        stable_click(3) 
        restore_mouse_pos(USR['start_pos'])



def F8():
    btype = 'Food_Preserver'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    item_pos = (175, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)
    else:
        output_error()

def F9():
    btype = 'DressMakery'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    item_pos = (-25, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)
    else:
        output_error()

def F10():
    btype = 'Rare_Tree_Plantation'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    if build:
        item_pos = (125, 50)
        if site == 'orange':
            build_item(*item_pos)
        elif site == 'green':
            build_item_L_M(*item_pos)
        else:
            output_error()
    if site == 'swirl':
        in_building_dialog(-285, 0) 
        stable_click(3)
        restore_mouse_pos(USR['start_pos'])

        

def F11():
    btype = 'Hunter_Gatherer'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    item_pos = (160, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error()

def F12():
    btype = 'Wilderness_Keeper'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    item_pos = (60, 95)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error()


def end():
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    btype = 'Furnace' if toggle_tab else 'Stone_Workshop'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)

    # Toggle changes only the item position
    item_pos = (75, 50) if toggle_tab else (175, 45)

    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)
    else:
        output_error()

def plus():
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    btype = 'Rope_Weaver' if toggle_tab else 'Liana_Cutter'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)

    # Toggle changes only the item position
    item_pos = (25, 45) if toggle_tab else (205, 45)
    if toggle_tab:#'Rope_Weaver'
        if site == 'orange':
            build_item(*item_pos)
        elif site == 'green':
            build_item_L_M(*item_pos)
        else:
            output_error()
    else:#'Liana_Cutter'
        if site == 'red':
            build_item(*item_pos)
        elif site == 'orange':
            build_item_M_S(*item_pos)
        elif site == 'green':
            build_item_L_S(*item_pos)
        else:
            output_error()

def equal():
    toggle_tab = transient_store_get('widelands_Toggle_Fkeys', False)
    btype = 'Warriors_Dwelling' if toggle_tab else 'Tower'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)

    # Toggle changes only the item position
    #      'Warriors_Dwelling'     else     'Tower' (default)
    item_pos = (125, 145) if toggle_tab else (175, 145)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_L_M(*item_pos)
    else:
        output_error()

def hyphen():
    btype = 'Patrol-Post'
    build, site = analyze_dialog(btype)
    update_USR(btype, site)
    item_pos = (160, 95)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error()
    
def backslash():
    # Dismantle Sites..
    update_USR('backslash_Dismantle', 'none')
    site = determine_dialog()
    if site == 'Garrison':
        in_building_dialog(-124,0)
    if site == 'Liana':
        in_building_dialog(-195,0)
    if site == 'Stonecutter':
        in_building_dialog(-235, 0)
    if site == 'Woodcutter':
        in_building_dialog(-165, 0)
    
def rightbracket():
    # Double Click
    update_USR('rightbracket', 'none')
    stable_click()
    time.sleep(0.1)
    stable_click()
    unpause_pause(0.08)

def leftbracket():
    # UPGRADING
    update_USR('leftbracket', 'none')
    site = determine_dialog()
    if site == 'Garrison':
        _, usite, var = get_screenshot_info(x=-188,y=0, method='id_dialog_icon')
        if usite == 'upgrade_icon':
            in_building_dialog(-188,0)
    if site == 'Woodcutter':
        in_building_dialog(-234, 0)
    if site == 'Lighter_brown':
        in_building_dialog(-206, 0)
    


def scroll_lock():
    update_USR('scroll_lock_Destroy', 'none')
    site = determine_dialog()
    if site == 'Garrison':
        in_building_dialog(-164,0)
    if site == 'Liana':
        in_building_dialog(-235,0)
    if site == 'Stonecutter':
        in_building_dialog(-275, 0)
    if site == 'Woodcutter':
        in_building_dialog(-205, 0)
