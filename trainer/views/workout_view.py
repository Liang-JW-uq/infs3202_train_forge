from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.db import transaction
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
    paginator = Paginator(workouts, 6)
    page_number = request.GET.get('page')
    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'trainer/workouts/workout_list.html', {'workouts': pager, 'search': search, 'page_obj': pager})


def workout_add(request):

    # Update the stepper
    request.session["module"] = 'workouts'
    # Retrieve the currently logged-in trainer object
    trainer = get_object_or_404(UserTrainer, id=request.user.id)

    # Check for the request method, if the page has just loaded or if it's submission time
    if request.method == "POST":

        # Create BOTH the Form and Formset
        ### !*REMINDER*!
        # A Formset is a Collection of MULTIPLE COPIES of the *Same Form* that are MANAGED TOGETHER as One Unit
        # We need this bcs Each Workout can have MULTIPLE EXERCISES RELATED TO IT
        # ... and for Every different Exercise, we need ONE UNIQUE WorkoutExercise Junction Data Entry
        form = WorkoutForm(request.POST, userTrainer = trainer)
        formset = WorkoutExerciseFormSet(request.POST, prefix='exercises')

        # Now we need to validate for BOTH Form + Formset before we continue
        if form.is_valid() and formset.is_valid():
            # Have to make sure there is at least one formset
            if len(formset.forms) > 0:
                try:
                    # Atomic means Either ALL SUCCEED, or ALL FAIL (Automatic Rollback if failure part-way)
                    with transaction.atomic():
                        # We have to save BEFORE doing anything, bcs the purpose of this line is to GET AN OBJECT TO SAVE TO IN THE FIRST PLACE
                        workout = form.save(commit=False)
                        # Once we have our object retrieved from the form data, NOW we have the base to save the currently logged-in trainer to
                        workout.trainer = trainer   # assign current trainer
                        # Now, we save properly once we have the trainer data
                        workout.save()

                        # Pass in the workout header as a property into the Formset (just accept the syntax)
                        formset.instance = workout
                        formset.save()

                    messages.success(request, "New workout created successfully!")
                    return redirect('workout_list')
                except ValidationError as e:
                    form.add_error(None, str(e))
                except Exception as e:
                    messages.error(request, f"Error: {str(e)}")
            else:
                form.add_error(None, "Must have at least one exercise")

        # This will hit if request==POST, BUT if the form isn't valid, or if there are errors found inside;
        # This will kick us back to the add page, but with the extra errors attached
        return render(request, 'trainer/workouts/workout_add.html', {
            'form': form,
            'formset': formset
        })
    
    else:
        form = WorkoutForm(userTrainer=trainer)
        formset = WorkoutExerciseFormSet()

    return render(request, 'trainer/workouts/workout_add.html', {'form': form, 'formset': formset})


def workout_edit(request, pk):
    # Saas tenant - get logged in trainer for data filtering
    trainer = get_object_or_404(UserTrainer, pk = request.user.id)
    # Since this is EDIT, we also retrieve the targeted Workout object
    workout = get_object_or_404(Workout, pk=pk, trainer = trainer)

    if request.method == "POST":
        # Instantiate both forms
        form = WorkoutForm(request.POST, instance=workout, userTrainer=trainer)
        formset = WorkoutExerciseFormSet(request.POST, instance=workout)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    formset.save()
                
                messages.success(request, "Workout updated!")
                
                return redirect('workout_list')
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")            
    else:
        form = WorkoutForm(instance=workout, userTrainer=trainer)
        formset = WorkoutExerciseFormSet(instance=workout)

    return render(request, 'trainer/workouts/workout_edit.html', {'form': form, 'formset': formset, 'workout': workout})

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

