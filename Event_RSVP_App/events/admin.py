### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Mini Project 4

from django.contrib import admin
from .models import Event, RSVP

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'organizer', 'capacity')
    list_filter = ('date_time', 'organizer')
    search_fields = ('title', 'location', 'organizer__username')

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('event__title', 'user__username')
