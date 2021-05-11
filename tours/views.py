from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseNotFound
from random import choice
from .data import tours as data_tours, departures as data_departures, title, subtitle, description


def custom_handler404(request, exception):
    return HttpResponseNotFound('Такой страницы не существует!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


def main_view(request):
    rand_tour_list = dict()
    while len(rand_tour_list) < 6:
        rand_tour_list.update([choice(list(data_tours.items()))])
    return render(request, 'index.html', {'title': title, 'subtitle': subtitle, 'tours': data_tours,
                                          'rand_tours': rand_tour_list, 'description': description, 'departures': data_departures})


def departure_view(request, departure):
    try:
        departure_from = data_departures[departure]
    except KeyError:
        return HttpResponseNotFound("Нет такого направления")

    departure_filtered = dict()
    for key, value in data_tours.items():
        if value['departure'] == departure:
            departure_filtered.update({key: value})

    tour_finded = len(departure_filtered)
    min_price = 0
    max_price = 0
    min_night = 0
    max_night = 0
    for key, value in departure_filtered.items():
        if not min_price and not min_night:
            min_price = value['price']
            min_night = value['nights']
        if value['price'] >= min_price:
            max_price = value['price']
        else:
            min_price = value['price']
        if value['nights'] >= min_night:
            max_night = value['nights']
        else:
            min_night = value['nights']

    return render(request, 'departure.html', {'departure': departure_from, 'departure_filtered': departure_filtered,
                                              'tour_finded': tour_finded, 'min_price': min_price,
                                              'max_price': max_price, 'min_night': min_night, 'max_night': max_night})


def tour_view(request, id):
    tours = data_tours[id]
    departures = data_departures
    stars_char = ''
    for i in range(int(tours['stars'])):
        stars_char += '★'
    return render(request, 'tour.html', {'tours': tours, 'departures': departures, 'stars_count': stars_char})


