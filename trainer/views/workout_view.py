from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from orm.models import Workout, WorkoutExercise, UserTrainer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.contrib import messages
from ..forms import WorkoutForm, WorkoutExerciseForm, WorkoutExerciseFormSet

def workout_list(request):
    request.session["module"] = 'workouts'

    trainer = get_object_or_404(UserTrainer, id=request.user.id)
    workouts = Workout.objects.filter(trainer=trainer)
    workouts = workouts.annotate(
        exercise_count = Count('exercises'),
        exercises_done = Count('exercises', filter=Q(exercises__is_done=True)),
    )
    
    search = request.GET.get('search', '')
    # We MUST order by something, otherwise will screw up paginator ordering when swapping pages
    if search:
        # icontains to ignore char case
        workouts = Workout.objects.filter(trainer=trainer, client__name__icontains=search).order_by('client__name').select_related("client")
    else:     
        workouts = Workout.objects.filter(trainer=trainer).order_by('client__name')

    # page controls - paginators with model data - 4 rows per page
    paginator = Paginator(workouts, 4)
    page_number = request.GET.get('page')
    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'trainer/workouts/workout_list.html', {'workouts': pager, 'search': search, 'page_obj': pager})


def workout_add(request):

    request.session["module"] = 'workouts'

    trainer = get_object_or_404(UserTrainer, id=request.user.id)
    if request.method == "POST":
        if form.is_valid():
            try:
                return redirect("workout_list")

            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = WorkoutForm()
        formset = WorkoutExerciseFormSet()

    return render(request, 'trainer/workouts/workout_add.html', {'form': form, 'formset': formset})


def workout_edit(request, pk):

    request.session["module"] = 'workouts'

    trainer = get_object_or_404(UserTrainer, id=request.user.id)
    workout = Workout.objects.get(id=pk, trainer=trainer)

    if request.method == "POST":
        if form.is_valid():
            try:
                return redirect("workout_list")

            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = WorkoutForm(instance=workout)
        formset = WorkoutExerciseFormSet()

    return render(request, 'trainer/workouts/workout_edit.html', {'form': form, 'formset': formset})


def workout_delete(request, pk):

    request.session["module"] = 'workouts'

    trainer = get_object_or_404(UserTrainer, id=request.user.id)
    workout = Workout.objects.get(id=pk, trainer=trainer)

    if request.method == "POST":
        try:
            workout.delete()
            messages.success(request, "Workout deleted successfully")
            return redirect("workout_list")
        except Exception as e:
            messages.error(request, f"Exceptions: {str(e)}")
    else:
        pass

    return render(request, 'trainer/workouts/workout_delete.html', {'workout': workout})

