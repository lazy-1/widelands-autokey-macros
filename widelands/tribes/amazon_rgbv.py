


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
    if (abs(r - 118) <= 10 and abs(g - 106) <= 10 and abs(b - 26) <= 10
        and 10000 < variance < 12500):# 'Gar' image
        return (False, 'Garrison')
    
    if (abs(r - 88) <= 3 and abs(g - 68) <= 3 and abs(b - 40) <= 3
        and 250 < variance < 500):# Blank brown image
        return (False, 'Standard_brown')
        
    if (abs(r - 96) <= 3 and abs(g - 76) <= 3 and abs(b - 45) <= 3
        and 250 < variance < 450):#Blank brown image Woodcutter is building dialog
        return (False, 'Lighter_brown')
        
    if (abs(r - 67) <= 5 and abs(g - 52) <= 5 and abs(b - 27) <= 5
        and 1800 < variance < 2500):# Tiny Liana icon
        return (False, 'Liana')

    if (abs(r - 70) <= 5 and abs(g - 58) <= 5 and abs(b - 40) <= 5
        and 3000 < variance < 4000):# Tiny StoneCutter icon
        return (False, 'Stonecutter')

    if (abs(r - 105) <= 5 and abs(g - 81) <= 5 and abs(b - 56) <= 5
        and 9000 < variance < 11500):# Tiny Woodcutter icon
        return (False, 'Woodcutter')
    
    return (False, f"({r}, {g}, {b}, {int(variance)})")  
    
