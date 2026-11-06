# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def registration_history(request):
    return render(
        request,
        'registrations/registration_history.html'
    )
