### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Mini Project 4

from django import forms
from django.utils import timezone
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

    def clean_date_time(self):
        date_time = self.cleaned_data['date_time']
        if date_time <= timezone.now():
            raise forms.ValidationError("Event date must be in the future.")
        return date_time


class RSVPForm(forms.Form):
    status = forms.ChoiceField(choices=RSVP_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
