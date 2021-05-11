from .data import departures as data_departures

def menu(request):
    return {'menu_links': data_departures}
