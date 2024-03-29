from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    """ Search Form Definition """

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class CreatePhotoForm(forms.ModelForm):

    """ CreatePhoto Form Definition """

    class Meta:
        model = models.Photo
        fields = ["caption", "file"]

    def save(self, pk, commit=True):
        photo = super().save(commit=commit)
        photo.room = models.Room.objects.get(pk=pk)
        photo.save()


class CreateRoomForm(forms.ModelForm):

    """ CreateRoom Form Definition """

    class Meta:
        model = models.Room
        fields = [
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
        ]

    def save(self, commit=True):
        return super().save(commit=commit)
