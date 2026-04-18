from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from ..forms import AppointmentForm

from orm.models import UserTrainer, Appointment

from django.db.models import Q

UserTrainer = get_user_model()

def appointment_list(request):

    request.session["module"] = 'appointment'

    trainer = UserTrainer.objects.get(id=request.user.id)
    
    search = request.GET.get('search', '')
    # We MUST order by something, otherwise will screw up paginator ordering when swapping pages
    if search:
        # icontains to ignore char case
        appointments = Appointment.objects.filter(trainer=trainer, client__name__icontains=search).order_by('client__name').select_related("client")
    else:     
        appointments = Appointment.objects.filter(trainer=trainer).order_by('client__name')

    # page controls - paginators with model data - 4 rows per page
    paginator = Paginator(appointments, 4)
    page_number = request.GET.get('page')
    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'trainer/appointments/appointment_list.html', {'appointments': pager, 'search': search, 'page_obj': pager})

def appointment_calendar(request):

    return render(request, "trainer/appointments/appointment_calendar.html")

def appointment_add(request):

    request.session["module"] = 'appointment'

    userTrainer = get_object_or_404(UserTrainer, id=request.user.id)

    # If coming from a calendar click, we might have a date in the URL
    initial_date = request.GET.get('date')

    if (request.method == "POST"):
        form = AppointmentForm(request.POST, userTrainer=userTrainer)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.trainer = userTrainer
                appointment.save()
                return redirect("appointment_calendar")
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = AppointmentForm(userTrainer=userTrainer, initial={"scheduled_date": initial_date})
        

    return render(request, "trainer/appointments/appointment_add.html", {"form": form})

def appointment_edit(request, pk):

    request.session["module"] = 'appointment'

    userTrainer = get_object_or_404(UserTrainer, id=request.user.id)
    appointment = Appointment.objects.get(trainer=userTrainer, id=pk)

    if (request.method == "POST"):
        form = AppointmentForm(request.POST, instance=appointment, userTrainer=userTrainer)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.trainer = userTrainer
                appointment.save()
                return redirect("appointment_calendar")
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = AppointmentForm(instance=appointment, userTrainer=userTrainer)

    return render(request, "trainer/appointments/appointment_edit.html", {"form": form})

def appointment_delete(request, pk):

    request.session["module"] = 'appointment'

    userTrainer = get_object_or_404(UserTrainer, id=request.user.id)
    appointment = Appointment.objects.get(trainer=userTrainer, id=pk)

    if request.method == "POST":
        try:
            appointment.delete()
            messages.success(request, "Appointment deleted successfully")
            return redirect("appointment_calendar")
        except Exception as e:
            messages.error(request, f"Exceptions: {str(e)}")
    else:
        pass

    return render(request, "trainer/appointments/appointment_delete.html")



def get_trainer_appointments(request):
    userTrainer = get_object_or_404(UserTrainer, id=request.user.id)
    appointments = Appointment.objects.filter(trainer=userTrainer)

    appointment_list = []
    for appointment in appointments:
        # https://fullcalendar.io/docs/event-object
        title_prefix = ""
        bg_color = ""
        if appointment.scheduled_time == "Morning":
            title_prefix = "(M)"
            bg_color = "#FFB20D"
        elif appointment.scheduled_time == "Afternoon":
            title_prefix = "(A)"
            bg_color = "#1334AD"
        else:
            title_prefix = "(N)"
            bg_color = "#AD3513"
        appointment_list.append({
            "id": appointment.id,
            "title": f"{title_prefix} {appointment.client.name}",
            "start": appointment.scheduled_date,
            "backgroundColor": bg_color,
            # "allDay": True,
            "url": f"/appointment/edit/{appointment.id}"
        })

    return JsonResponse(appointment_list, safe=False)