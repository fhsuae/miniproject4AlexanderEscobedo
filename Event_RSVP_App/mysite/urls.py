### mysite/urls.py ###
### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Mini Project 4


from django.contrib import admin
from django.urls import include, path
from events import views as event_views  # For signup view

urlpatterns = [
    path("events/", include("events.urls")),
    path("accounts/", include("django.contrib.auth.urls")),  # login, logout, etc.
    path("accounts/signup/", event_views.signup, name="signup"),
    path('admin/', admin.site.urls),
]
