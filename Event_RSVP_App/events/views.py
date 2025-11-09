### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Mini Project 4

from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

from .models import Event, RSVP
from .forms import EventForm, RSVPForm  # You'll create these forms

def home(request):
    return render(request, "home.html")

class IndexView(generic.ListView):
    model = Event
    template_name = "events/index.html"
    context_object_name = "event_list"

    def get_queryset(self):
        # Annotate events with count of attendees who RSVP'd "Going"
        return Event.objects.annotate(
            attendee_count=Count('rsvp', filter=Q(rsvp__status='Going'))
        ).order_by("date_time")

def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        form = RSVPForm(request.POST)
        if form.is_valid():
            rsvp, created = RSVP.objects.update_or_create(
                event=event,
                user=request.user,
                defaults={"status": form.cleaned_data["status"]},
            )
            return HttpResponseRedirect(reverse("events:detail", args=[event_id]))
    else:
        form = RSVPForm()

    user_rsvp = None
    if request.user.is_authenticated:
        try:
            user_rsvp = RSVP.objects.get(event=event, user=request.user)
        except RSVP.DoesNotExist:
            user_rsvp = None

    context = {
        "event": event,
        "form": form,
        "user_rsvp": user_rsvp,
    }
    return render(request, "events/detail.html", context)

@method_decorator(login_required, name='dispatch')
class CreateEventView(generic.View):
    def get(self, request):
        form = EventForm()
        return render(request, "events/create_event.html", {"form": form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect("events:detail", event_id=event.id)
        return render(request, "events/create_event.html", {"form": form})

@login_required
@require_POST
def create_event_ajax(request):
    form = EventForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

@method_decorator(login_required, name='dispatch')
class MyEventsView(generic.ListView):
    model = Event
    template_name = "events/my_events.html"
    context_object_name = "my_events"

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user).order_by("date_time")

@login_required
def attendees(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.organizer != request.user:
        return HttpResponseRedirect(reverse("events:index"))

    rsvps = RSVP.objects.filter(event=event).order_by("-timestamp")
    return render(request, "events/attendees.html", {"event": event, "rsvps": rsvps})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('events:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
