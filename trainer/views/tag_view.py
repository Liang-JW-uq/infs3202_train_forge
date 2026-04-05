from django.shortcuts import render, redirect
from django.db.models import Count
from orm.models import Tag, UserTrainer

def tag_list(request):

    userTrainer = UserTrainer.objects.get(id=request.user.id)
    tags = Tag.objects.filter(trainer=userTrainer)
    tags =  tags.annotate(exercise_count = Count('tags_exercises'))

    return render(request, "trainer/tags/tag_list.html", {"tags": tags})

def tag_add(request):
    userTrainer = UserTrainer.objects.get(id=request.user.id)
    if request.method == "POST":
        pass
    else:
        pass

    return render(request, "trainer/tags/tag_add.html", {})

def tag_edit(request):
    userTrainer = UserTrainer.objects.get(id=request.user.id)
    if request.method == "POST":
        pass
    else:
        pass


    return render(request, "trainer/tags/tag_edit.html", {})

def tag_delete(request):
    userTrainer = UserTrainer.objects.get(id=request.user.id)
    if request.method == "POST":
        pass
    else:
        pass


    return render(request, "trainer/tags/tag_delete.html", {})