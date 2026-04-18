from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from orm.models import UserTrainer, Tag, Exercise, Client, Workout

def home(request):
    userTrainer = get_object_or_404(UserTrainer, pk=request.user.id)
    tags_count = Tag.objects.filter(trainer=userTrainer).count()
    exercise_count = Exercise.objects.filter(trainer=userTrainer).count()
    client_count = Client.objects.filter(trainer=userTrainer).count()
    workout_count = Workout.objects.filter(trainer=userTrainer).count()

    workouts = Workout.objects.filter(trainer=userTrainer)
    workouts = workouts.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        pending=Count('id', filter=Q(is_completed=False))
    )

    summary = {
        "tags_count": tags_count,
        "exercise_count": exercise_count,
        "client_count": client_count,
        "workouts": workouts
    }

    return render(request, "trainer/home.html", {"summary": summary})