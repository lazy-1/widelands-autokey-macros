      
# Atlantean

# ===============================================
# Atlantean FUNCTIONS (F1–F12 + end + hyphen + equal + backslash + rightbracket)
# ===============================================


def F1():
    btype = 'Quarry'
    build, site = analyze_dialog(btype)
    #build, site = analyze_dialog(btype,func1=id_dialog_icon2)
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
