### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Mini Project 4

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')

    def __str__(self):
        return f"{self.title} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"

    def spots_left(self):
        going_count = self.rsvp_set.filter(status='Going').count()
        return self.capacity - going_count

    def is_full(self):
        return self.spots_left() <= 0

class RSVP(models.Model):
    STATUS_CHOICES = [
        ('Going', 'Going'),
        ('Maybe', 'Maybe'),
        ('Not Going', 'Not Going'),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Maybe')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} RSVP'd {self.status} to {self.event.title}"
