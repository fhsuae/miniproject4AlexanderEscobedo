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
from django.contrib import messages  # For flash messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

from .models import Event, RSVP
from .forms import EventForm, RSVPForm  # Forms for creating events and RSVPs

def home(request):
    """Render the home page."""
    return render(request, "home.html")

class IndexView(generic.ListView):
    """Display a list of upcoming events with attendee counts."""
    model = Event
    template_name = "events/index.html"
    context_object_name = "event_list"

    def get_queryset(self):
        # Annotate events with count of attendees who RSVP'd "Going"
        return Event.objects.annotate(
            attendee_count=Count('rsvp', filter=Q(rsvp__status='Going'))
        ).order_by("date_time")

def detail(request, event_id):
    """
    Display event details and handle RSVP submissions.
    Only authenticated users can RSVP.
    """
    event = get_object_or_404(Event, pk=event_id)

    # Count current "Going" RSVPs to check capacity
    going_count = RSVP.objects.filter(event=event, status='Going').count()

    if request.method == "POST":
        # Redirect to login if user is not authenticated
        if not request.user.is_authenticated:
            return redirect('login')

        form = RSVPForm(request.POST)
        if form.is_valid():
            desired_status = form.cleaned_data["status"]
            user_already_rsvp = RSVP.objects.filter(event=event, user=request.user).first()

            # If trying to RSVP "Going", check capacity and allow changes
            if desired_status == "Going":
                if going_count >= event.capacity:
                    # Allow if user is already "Going" to change status
                    if not (user_already_rsvp and user_already_rsvp.status == "Going"):
                        messages.error(request, "Sorry, this event is already at full capacity.")
                        context = {
                            "event": event,
                            "form": form,
                            "user_rsvp": user_already_rsvp,
                        }
                        return render(request, "events/detail.html", context)

            # Save or update RSVP record
            rsvp, created = RSVP.objects.update_or_create(
                event=event,
                user=request.user,
                defaults={"status": desired_status},
            )
            messages.success(request, "Your RSVP has been updated!")
            return HttpResponseRedirect(reverse("events:detail", args=[event_id]))
    else:
        form = RSVPForm()

    # Get existing RSVP for user to show in the template
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
    """View to display the create event form and handle its submission (non-AJAX)."""

    def get(self, request):
        form = EventForm()
        return render(request, "events/create_event.html", {"form": form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect("events:detail", event_id=event.id)
        return render(request, "events/create_event.html", {"form": form})

@require_POST
def create_event_ajax(request):
    """
    AJAX endpoint for creating an event.
    Returns JSON success or error responses.
    Requires user to be logged in.
    """
    # Check if user is authenticated before processing form
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "errors": {"__all__": ["You must be logged in to create an event."]}
            },
            status=403
        )

    form = EventForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.save()
        messages.success(request, "Event created successfully!")
        return JsonResponse({"success": True})
    else:
        # Return form errors as JSON with 400 status
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

@method_decorator(login_required, name='dispatch')
class MyEventsView(generic.ListView):
    """List view for events organized by the logged-in user."""
    model = Event
    template_name = "events/my_events.html"
    context_object_name = "my_events"

    def get_queryset(self):
        # Filter events by organizer
        return Event.objects.filter(organizer=self.request.user).order_by("date_time")

@login_required
def attendees(request, event_id):
    """
    Display a list of attendees for an event.
    Only accessible by the event organizer.
    """
    event = get_object_or_404(Event, pk=event_id)
    if event.organizer != request.user:
        # Redirect if user is not the organizer
        return HttpResponseRedirect(reverse("events:index"))

    rsvps = RSVP.objects.filter(event=event).order_by("-timestamp")
    return render(request, "events/attendees.html", {"event": event, "rsvps": rsvps})

def signup(request):
    """
    User signup view.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log the user in after signup
            return redirect('events:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
