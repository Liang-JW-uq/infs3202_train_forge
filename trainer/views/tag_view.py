from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from orm.models import Tag, UserTrainer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import JsonResponse

from ..forms import TagForm

def tag_list(request):

    request.session["module"] = 'tags'

    userTrainer = UserTrainer.objects.get(id=request.user.id)

    search = request.GET.get('search', '')
    # We MUST order by something, otherwise will screw up paginator ordering when swapping pages
    if search:
        # icontains to ignore char case
        tags = Tag.objects.filter(trainer=userTrainer, name__icontains=search).order_by('name')
    else:     
        tags = Tag.objects.filter(trainer=userTrainer).order_by('name')

    # tags = Tag.objects.filter(trainer=userTrainer)
    tags =  tags.annotate(exercise_count = Count('exercises'))


    # page controls - paginators with model data - 4 rows per page
    paginator = Paginator(tags, 6)
    page_number = request.GET.get('page')
    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'trainer/tags/tag_list.html', {'tags': pager, 'search': search, 'page_obj': pager})

def tag_add(request):
    userTrainer = UserTrainer.objects.get(id=request.user.id)
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            try:
                # tag = form.save() # We CANNOT call save YET becoz we need Trainer to complete the Object Model before saving
                tag = form.save(commit=False)
                tag.trainer = userTrainer
                tag.save()
                # 'messages' go to base.html
                messages.success(request, "Tag added successfully")
                return redirect("tag_list")
            except ValidationError as e:
                # Errors here are triggered by the FORM CONSTRAINTS;
                # Also catches DUPLICATES even if not outside constraints because MODEL CONSTRAINTS;
                # form.add_error goes to the local HTML template page, NOT the form file
                # Search for 'form_error' in the local files
                form.add_error(None, str(e))
            except Exception as e:
                # Errors here are triggered by EXTERNAL SOURCES [Hard DB col restrictions, connection fail, etc]
                messages.error(request, f"Exceptions: {str(e)}")
        else:
            form.add_error(None, "Invalid Form!")

    else:
        form = TagForm()

    return render(request, "trainer/tags/tag_add.html", {"form": form})

def tag_edit(request, pk):
    userTrainer = UserTrainer.objects.get(id=request.user.id)
    tag = Tag.objects.get(id=pk, trainer=userTrainer)
    affected_exercises = tag.exercises.all()

    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            try:
                tag = form.save(commit=False)
                tag.trainer = userTrainer
                tag.save()
                messages.success(request, "Tag updated successfully")
                return redirect("tag_list")
            except ValidationError as e:
                    form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = TagForm(instance=tag)


    return render(request, "trainer/tags/tag_edit.html", {"form": form, "affected_exercises": affected_exercises})

def tag_delete(request, pk):
    userTrainer = UserTrainer.objects.get(id=request.user.id)
    tag = Tag.objects.get(id=pk, trainer=userTrainer)

    if request.method == "POST":
        try:
            tag.delete()
            messages.success(request, "Tag deleted successfully")
            return redirect("tag_list")
        except Exception as e:
            messages.error(request, f"Exceptions: {str(e)}")
    else:
        pass

    return render(request, "trainer/tags/tag_delete.html", {"tag": tag})

def get_trainer_tags(request):
    trainer = get_object_or_404(UserTrainer, id=request.user.id)
    tags = Tag.objects.filter(trainer=trainer).order_by("id")
    # tag_list = []
    # for tag in tags:
    #     tag_list.append({"id": tag.id, "name": tag.name})
    # id = client_info['id']
    # id = client_info.get('id')

    # return JsonResponse(tag_list, safe=False)
    return render(request, 'trainer/partials/_tag_partial.html', {'tags': tags})