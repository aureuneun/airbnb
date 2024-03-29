from django import template
from .. import models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    the_list = models.List.objects.get_or_none(
        user=user,
        name="My Favourites Houses",
    )
    if the_list is not None:
        return room in the_list.rooms.all()
    return False
