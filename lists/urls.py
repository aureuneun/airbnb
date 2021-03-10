from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("toggle-room/<int:pk>/", views.toggle_room_view, name="toggle-room"),
    path("favs/", views.SeeFavsView.as_view(), name="see-favs"),
]
