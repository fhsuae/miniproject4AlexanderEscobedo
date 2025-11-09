### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Mini Project 4

from django.contrib import admin
from .models import Event, RSVP

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'organizer', 'capacity', 'spots_left', 'is_full')
    list_filter = ('date_time', 'organizer')
    search_fields = ('title', 'location', 'organizer__username')
    date_hierarchy = 'date_time'
    readonly_fields = ('spots_left_display', 'is_full_display')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'organizer')
        }),
        ('Event Details', {
            'fields': ('date_time', 'location', 'capacity')
        }),
        ('Attendance Info', {
            'fields': ('spots_left_display', 'is_full_display'),
            'classes': ('collapse',)
        }),
    )

    def spots_left(self, obj):
        return obj.spots_left()
    spots_left.short_description = 'Spots Left'

    def is_full(self, obj):
        return "Yes" if obj.is_full() else "No"
    is_full.short_description = 'Full?'

 #  Methods for detail view
    def spots_left_display(self, obj):
        return obj.spots_left()
    spots_left_display.short_description = 'Spots Left'

    def is_full_display(self, obj):
        return "Yes" if obj.is_full() else "No"
    is_full_display.short_description = 'Is Event Full?'

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'timestamp')
    list_filter = ('status', 'timestamp', 'event')
    search_fields = ('event__title', 'user__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)

# Group by event in the list view
    list_select_related = ('event', 'user')