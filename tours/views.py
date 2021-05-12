from random import choice

from django.http import HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render

from .data import tours as data_tours, departures as data_departures, title, subtitle, description


def custom_handler404(request, exception):
    return HttpResponseNotFound('Такой страницы не существует!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


def main_view(request):
    rand_tour_list = dict()
    while len(rand_tour_list) < 6:
        rand_tour_list.update([choice(list(data_tours.items()))])

    return render(request, 'index.html', {'title': title, 'subtitle': subtitle, 'rand_tours': rand_tour_list,
                                          'description': description})


def departure_view(request, departure):
    try:
        departure_from = data_departures[departure]
    except KeyError:
        return HttpResponseNotFound("Нет такого направления")

    departure_filtered = dict()
    for id_hotel, hotel in data_tours.items():
        if hotel['departure'] == departure:
            departure_filtered.update({id_hotel: hotel})

    tour_finded = len(departure_filtered)
    night_dict = dict()
    price_dict = dict()
    for key, value in departure_filtered.items():
        night_dict.update({key: value['nights']})
        price_dict.update({key: value['price']})
    max_night = max(night_dict.values())
    min_night = min(night_dict.values())
    max_price = max(price_dict.values())
    min_price = min(price_dict.values())

    return render(request, 'departure.html', {'departure': departure_from, 'departure_filtered': departure_filtered,
                                              'tour_finded': tour_finded, 'min_price': min_price,
                                              'max_price': max_price, 'min_night': min_night, 'max_night': max_night})


def tour_view(request, id):
    tours = data_tours[id]
    stars_char = ''
    for i in range(int(tours['stars'])):
        stars_char += '★'

    return render(request, 'tour.html', {'tours': tours, 'departures': data_departures, 'stars_count': stars_char})
