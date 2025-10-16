from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Seat, Session, Plan

def index(request):
    seats = Seat.objects.order_by('number')
    open_sessions = {s.seat.number: s for s in Session.objects.filter(end_at__isnull=True)}
    plans = Plan.objects.all()
    return render(request, 'seats/index.html', {
        'seats': seats,
        'open_sessions': open_sessions,
        'plans': plans,
    })

def start_session(request, seat_number):
    seat = get_object_or_404(Seat, number=seat_number)
    if request.method == 'POST':
        plan_id = int(request.POST['plan'])
        plan = get_object_or_404(Plan, id=plan_id)
        if Session.objects.filter(seat=seat, end_at__isnull=True).exists():
            return redirect('index')
        Session.objects.create(seat=seat, plan=plan, start_at=timezone.now())
    return redirect('index')

def end_session(request, seat_number):
    seat = get_object_or_404(Seat, number=seat_number)
    session = Session.objects.filter(seat=seat, end_at__isnull=True).first()
    if session:
        session.end_session()
    return redirect('index')
