from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .workout import Workout
from .exercise import Exercise

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name="exercises" # Each workout can have multiple exercises
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="exercise_workout_exercise" # Each junction object points to its own exercise
    )
    sets = models.IntegerField(
        db_default=0,
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    reps = models.IntegerField(
        db_default=0,
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    weight = models.IntegerField(
        db_default=0,
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    duration = models.IntegerField(
        db_default=0,
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    actual_sets = models.IntegerField(
        db_default=0,
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    actual_reps = models.IntegerField(
        db_default=0,
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    actual_weight = models.IntegerField(
        db_default=0,
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    actual_duration = models.IntegerField(
        db_default=0,
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )


    class Meta:
        db_table="workouts_exercises"

    def __str__(self):
        return "Placeholder"