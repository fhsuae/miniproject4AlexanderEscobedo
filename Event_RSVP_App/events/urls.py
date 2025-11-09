### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Mini Project 4


from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:event_id>/", views.detail, name="detail"),
    path("create/", views.CreateEventView.as_view(), name="create_event"),
    path("my_events/", views.MyEventsView.as_view(), name="my_events"),
    path("<int:event_id>/attendees/", views.attendees, name="attendees"),
]
