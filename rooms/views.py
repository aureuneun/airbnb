from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    ordering = "created"


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    s_city = str.capitalize(city)
    s_country = request.GET.get("country", "KR")
    s_room_type = int(request.GET.get("room_type", 0))
    s_price = int(request.GET.get("price", 0))
    s_guests = int(request.GET.get("guests", 0))
    s_beds = int(request.GET.get("beds", 0))
    s_bedrooms = int(request.GET.get("bedrooms", 0))
    s_baths = int(request.GET.get("baths", 0))
    s_instant = bool(request.GET.get("instant", False))
    s_superhost = bool(request.GET.get("superhost", False))
    s_amenities = list(map(int, request.GET.getlist("amenities")))
    s_facilities = list(map(int, request.GET.getlist("facilities")))
    form = {
        "s_city": s_city,
        "s_country": s_country,
        "s_room_type": s_room_type,
        "s_price": s_price,
        "s_guests": s_guests,
        "s_beds": s_beds,
        "s_bedrooms": s_bedrooms,
        "s_baths": s_baths,
        "s_instant": s_instant,
        "s_superhost": s_superhost,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
    }
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }
    filter_args = {}
    if s_city != "Anywhere":
        filter_args["city__startswith"] = s_city
    filter_args["country"] = s_country
    if s_room_type != 0:
        filter_args["room_type__pk"] = s_room_type
    if s_price != 0:
        filter_args["price__lte"] = s_price
    if s_guests != 0:
        filter_args["guests__gte"] = s_guests
    if s_beds != 0:
        filter_args["beds__gte"] = s_beds
    if s_bedrooms != 0:
        filter_args["bedrooms__gte"] = s_bedrooms
    if s_baths != 0:
        filter_args["baths__gte"] = s_baths
    if s_instant:
        filter_args["instant_book"] = True
    if s_superhost:
        filter_args["host__superhost"] = True
    rooms = models.Room.objects.filter(**filter_args)
    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            rooms = rooms.filter(amenities__pk=s_amenity)
    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            rooms = rooms.filter(facilities__pk=s_facility)
    return render(
        request,
        "rooms/search.html",
        {**form, **choices, "rooms": rooms},
    )
