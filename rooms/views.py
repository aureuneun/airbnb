from django.views.generic import ListView, DetailView
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room
