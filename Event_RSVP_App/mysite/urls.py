### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Mini Project 4

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from events import views as event_views  # For signup view

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),  # <-- homepage
    path("events/", include("events.urls")),
    path("accounts/", include("django.contrib.auth.urls")),  # login, logout, etc.
    path("accounts/signup/", event_views.signup, name="signup"),
    path("admin/", admin.site.urls),
]