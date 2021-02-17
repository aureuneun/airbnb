from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import models


def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        return redirect("/")
    except EmptyPage:
        return redirect("/")
    return render(
        request,
        "rooms/home.html",
        {"pages": pages},
    )
