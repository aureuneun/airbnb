from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from rooms import models as room_models
from . import models


def toggle_room_view(request, pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=pk)
    if room is not None and action is not None:
        the_list, created = models.List.objects.get_or_create(
            user=request.user, name="My Favourites Houses"
        )
        if action == "add":
            the_list.rooms.add(room)
        elif action == "remove":
            the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": pk}))


class SeeFavsView(TemplateView):

    """ SeeFavs View Definition """

    template_name = "lists/list_detail.html"
