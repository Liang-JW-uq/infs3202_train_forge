from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.db import transaction
from orm.models import Tag, Exercise, UserTrainer
from django.core.exceptions import ValidationError
from django.contrib import messages

from ..forms import ExerciseForm

def exercise_list(request):
    
    request.session["module"] = 'exercises'

    trainer = UserTrainer.objects.get(id=request.user.id)
    
    search = request.GET.get('search', '')
    # We MUST order by something, otherwise will screw up paginator ordering when swapping pages
    if search:
        # icontains to ignore char case
        exercises = Exercise.objects.filter(trainer=trainer, name__icontains=search).order_by('name')
    else:     
        exercises = Exercise.objects.filter(trainer=trainer).order_by('name')

    # tags = Tag.objects.filter(trainer=userTrainer)
    # tags =  tags.annotate(exercise_count = Count('tags_exercises'))

    # page controls - paginators with model data - 4 rows per page
    paginator = Paginator(exercises, 4)
    page_number = request.GET.get('page')
    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'trainer/exercises/exercise_list.html', {'exercises': pager, 'search': search, 'page_obj': pager})

def exercise_add(request):

    request.session["module"] = 'exercises'
    
    userTrainer = UserTrainer.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, userTrainer=userTrainer)
        if form.is_valid():
            try:
                # Atomic is to ensure that BOTH exercise.save() and the junction table form.save() are carried out before committing
                # Otherwise we could get an error halfway through and save one part but not the other, then have inconsistency in data
                with transaction.atomic():
                    exercise = form.save(commit=False)
                    exercise.trainer = userTrainer
                    exercise.save()

                    # This is needed to automatically save the Tags we selected, since it's a M2M relationship
                    form.save_m2m()

                messages.success(request, "Exercise updated successfully")
                return redirect("exercise_list")
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
        
    else:
        # Here, when first rendering the form, we PASS BACK THE CURRENTLY LOGGED-IN TRAINER
        # ... BACK TO THE FORM so we know ** WHICH TAGS TO INCLUDE **
        # We can access Trainer Details here using *request.user.id*, but the FORM is ISOLATED, so we have to pass in from here
        form = ExerciseForm(userTrainer=userTrainer)

    # This is the HTML, we CANNOT pass in the Trainer to populate the Form from here
    # ... because the HTML itself also RELIES ON THE FORM to *Generate Field Details*
    return render(request, "trainer/exercises/exercise_add.html", {"form": form})

def exercise_edit(request, pk):

    request.session["module"] = 'exercises'

    userTrainer = UserTrainer.objects.get(id=request.user.id)

    # Make sure to get the exercise to edit as well
    exercise = get_object_or_404(Exercise, pk=pk, trainer=userTrainer)

    # !!! OUTDATED !!!   NEW METHODOLOGY USED TO FIND TAGS
    # # Reverse lookup ;
    # #   1) related_name first, NO NEED TABLE FOR THE FIRST R-L ITEM;
    # #   2) ... then FK-COLUMN name IN THE NEXT TABLE,
    # #   3) ... then column of that table
    # tags = Tag.objects.filter(tags_exercises__exercise__id=1)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise, userTrainer=userTrainer)
        if form.is_valid():
            try:
                with transaction.atomic():
                    exercise = form.save(commit=False)
                    exercise.trainer = userTrainer
                    exercise.save()

                    # Like above, this will handle all of the necessary junction table actions automatically
                    form.save_m2m()

                messages.success(request, "Exercise updated successfully")
                return redirect("exercise_list")
            except ValidationError as e:
                    form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")

    else:
        form = ExerciseForm(instance=exercise, userTrainer=userTrainer)
    return render(request, "trainer/exercises/exercise_edit.html", {"form": form})

def exercise_delete(request, pk):

    request.session["module"] = 'exercises'

    userTrainer = UserTrainer.objects.get(id=request.user.id)
    exercise = Exercise.objects.filter(trainer=userTrainer, id=pk)
    if request.method == 'POST':
        try:
            exercise.delete()
            messages.success(request, "Tag deleted successfully")
            return redirect("tag_list")
        except Exception as e:
            messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, "trainer/exercises/exercise_delete.html", {"form": form})