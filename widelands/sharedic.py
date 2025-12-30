# shared dictionary 

CONTEXT = {
    'tribe': None,
    'keyboard': None,
    'building': None,
    'icon': None,
    'start_pos': None,
}
def _set_io(building, icon):
    CONTEXT['building'] = building
    CONTEXT['icon'] = icon
