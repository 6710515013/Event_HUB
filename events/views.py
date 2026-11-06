
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Event
from .forms import EventForm


@login_required(login_url="login")
def event_create(request):

    if request.user.role != "ORGANIZER":
        return HttpResponseForbidden(
            "You do not have permission to access this page."
        )

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            form.save_m2m()

            return redirect("events:event_list")

    else:
        form = EventForm()

    return render(
        request,
        "events/event_form.html",
        {"form": form}
    )


@login_required(login_url="login")
def event_list(request):

    if request.user.role != "ORGANIZER":
        return HttpResponseForbidden(
            "You do not have permission to access this page."
        )

    events = Event.objects.filter(
        created_by=request.user
    )

    return render(
        request,
        "events/event_list.html",
        {"events": events}
    )


@login_required(login_url="login")
def event_edit(request, event_id):

    if request.user.role != "ORGANIZER":
        return HttpResponseForbidden(
            "You do not have permission to access this page."
        )

    event = get_object_or_404(
        Event,
        pk=event_id,
        created_by=request.user
    )

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)

        if form.is_valid():
            form.save()

            return redirect("events:event_list")

    else:
        form = EventForm(instance=event)

    return render(
        request,
        "events/event_form.html",
        {
            "form": form,
            "event": event
        }
    )

@login_required(login_url="login")
def event_delete(request, event_id):

    if request.user.role != "ORGANIZER":
        return HttpResponseForbidden(
            "You do not have permission to access this page."
        )

    event = get_object_or_404(
        Event,
        pk=event_id,
        created_by=request.user
    )

    if request.method == "POST":
        event.delete()
        return redirect("events:event_list")

    return render(
        request,
        "events/event_confirm_delete.html",
        {"event": event}
    )
