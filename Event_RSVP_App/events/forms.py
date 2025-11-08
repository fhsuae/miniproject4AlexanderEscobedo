### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Mini Project 4

from django import forms
from .models import Event

RSVP_CHOICES = [
    ("Going", "Going"),
    ("Maybe", "Maybe"),
    ("Not Going", "Not Going"),
]

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date_time", "location", "capacity"]

        widgets = {
            "date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class RSVPForm(forms.Form):
    status = forms.ChoiceField(choices=RSVP_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
