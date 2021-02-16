from math import ceil
from django.shortcuts import render
from . import models


def all_rooms(request):
    pagination = 10
    page = int(request.GET.get("page") or 1)
    if page > 0:
        offset = (page - 1) * pagination
    else:
        page = 1
        offset = 0
    limit = offset + pagination
    rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / pagination)
    return render(
        request,
        "rooms/home.html",
        {
            "rooms": rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    )
