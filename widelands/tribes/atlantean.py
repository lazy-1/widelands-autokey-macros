      
# Atlantean

# ===============================================
# Atlantean FUNCTIONS (F1–F12 + end + hyphen + equal + backslash + rightbracket)
# ===============================================
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

def F1():
    btype = 'Quarry'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (5, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error()

def F2():
    btype = 'Woodcutter'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (60, 45)  # standardised Y to match most buildings
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error()

def F3():
    btype = 'Forester'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (105, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error()

def F4():
    btype = 'Well'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (60, 95)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error()

def F5():
    btype = 'Bakery'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (175, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        output_error()

def F6():
    btype = 'Smokery'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (75, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        output_error()

def F7():
    btype = 'Mill'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (125, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        output_error()

def F8():
    btype = 'Smelter'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (20, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        output_error()

def F9():
    btype = 'Weaponsmith'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (125, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        output_error()

def F10():
    btype = 'Armoursmith'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (175, 95)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        output_error()

def F11():
    btype = 'Fish'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (155, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error()

def F12():
    btype = 'Fishbreader'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (205, 45)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error()

def end():
    btype = 'SawMill'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (25, 50)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        output_error()

def hyphen():
    btype = 'Guardhouse'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (200, 100)
    if site == 'red':
        build_item(*item_pos)
    elif site == 'orange':
        build_item_M_S(*item_pos)
    elif site == 'green':
        build_item_L_S(*item_pos)
    else:
        output_error()

def equal():
    btype = 'Tower'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    item_pos = (125, 145)
    if site == 'orange':
        build_item(*item_pos)
    elif site == 'green':
        build_item_M_S(*item_pos)
    else:
        output_error()

def plus():
    btype = 'Charcoal Kiln'
    build, site = analyze_dialog(btype)
    _set_io(btype, site)
    if build:
        item_pos = (-25, 95)
        if site == 'orange':
            build_item(*item_pos)
        elif site == 'green':
            build_item_L_M(*item_pos)
        else:
            output_error()   
    if site == 'Charcoal_kiln':
        in_building_dialog(-174, 20) 
        stable_click(3)
        restore_mouse_pos(CONTEXT['start_pos'])

def leftbracket():
    # UPGRADING
    _set_io('Amazon_leftbracket', 'none')
    site = determine_dialog()
    if site == 'Garrison':
        _, usite, var = get_screenshot_info(x=-188,y=0, method='id_dialog_icon')
        if usite == 'upgrade_tower':
            in_building_dialog(-188,0)

def rightbracket():
    # Double Click
    _set_io('rightbracket', 'none')
    stable_click()
    time.sleep(0.1)
    stable_click()
    unpause_pause(0.08)

def backslash():
    # Dismantle Guardhouse, Tower, Castle etc...
    _set_io('Dismantle', 'none')
    site = determine_dialog()
    if site == 'Garrison':
        in_building_dialog(-124,0)
    elif site in ['Woodcutter','Forester','Quary','Fishbreeder','Fish','Well']:
        in_building_dialog(-235, 0)
    elif site == 'Scout':
        in_building_dialog(-48, 36)
        
def scroll_lock():
     # Destroy! Guardhouse, Tower, Castle etc...
    _set_io('Amazon_scroll_lock_Destroy', 'none')
    site = determine_dialog()
    if site == 'Garrison':
        in_building_dialog(-164,0)
    elif site in ['Woodcutter','Forester','Quary','Fishbreeder','Fish','Well']:
        in_building_dialog(-265, 0)
    elif site == 'Scout':
        in_building_dialog(-84, 36)
