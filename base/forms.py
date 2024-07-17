from django.forms import ModelForm
from .models import Movie

class RoomForm(ModelForm):
    class Meta:
        model= Movie
        fields='__all__'
        exclude =['host','particpants']
