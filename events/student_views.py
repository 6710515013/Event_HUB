from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from events.models import Event


def get_filtered_events(request):
    """ค้นหาและกรองกิจกรรมสำหรับ Student"""

    query = request.GET.get("q", "").strip()
    date = request.GET.get("date", "").strip()

    # แสดงเฉพาะกิจกรรมที่เปิดรับสมัคร
    events = Event.objects.filter(status=Event.Status.OPEN)

    # ค้นหาจากชื่อกิจกรรม
    if query:
        events = events.filter(title__icontains=query)

    # กรองตามวันที่เริ่มกิจกรรม
    if date:
        events = events.filter(start_datetime__date=date)

    return events


@login_required
def event_list(request):
    """แสดงรายการกิจกรรมสำหรับ Student"""

    events = get_filtered_events(request)

    return render(
        request,
        "events/student_list.html",
        {
            "events": events,
            "query": request.GET.get("q", "").strip(),
            "selected_date": request.GET.get("date", "").strip(),
        },
    )


@login_required
def event_detail(request, event_id):
    """แสดงรายละเอียดกิจกรรม"""

    event = get_object_or_404(Event, pk=event_id)

    can_register = (
        event.status == Event.Status.OPEN
        and timezone.now() <= event.registration_deadline
    )

    return render(
        request,
        "events/student_detail.html",
        {
            "event": event,
            "can_register": can_register,
        },
    )