from django.db import models

from .workout import Workout
from .exercise import Exercise

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, EmailValidator

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout, 
        on_delete=models.CASCADE, 
        related_name="exercises"
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete = models.RESTRICT,
        related_name = 'workout_exercises'
    )

    is_done = models.BooleanField(db_default=False)

    # prescribed workout
    pre_sets = models.PositiveIntegerField(
        default=0,
        db_default=0,
        validators = [MinValueValidator(0), MaxValueValidator(100)]
    )
    pre_reps = models.PositiveIntegerField(
        default=0,
        db_default=0,
        validators = [MinValueValidator(0), MaxValueValidator(200)]
    )
    pre_weight = models.DecimalField(
        default=0,
        db_default=0,
        blank=True,
        max_digits = 5,
        decimal_places = 2,
        validators = [MinValueValidator(0), MaxValueValidator(200)]
    )
    pre_duration = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True
    )

    # actual done
    actual_sets = models.PositiveIntegerField(
        default=0,
        db_default=0,
        validators = [MinValueValidator(0), MaxValueValidator(100)],
        blank=True
    )
    actual_reps = models.PositiveIntegerField(
        default=0,
        db_default=0,
        validators = [MinValueValidator(0), MaxValueValidator(200)],
        blank=True
    )
    actual_weight = models.DecimalField(
        default=0,
        db_default=0,
        blank=True,
        max_digits = 5,
        decimal_places = 2,
        validators = [MinValueValidator(0), MaxValueValidator(200)],
    )
    actual_duration = models.PositiveIntegerField(
        default=0,
        db_default=0,
        blank=True
    )


    class Meta:
        unique_together = ['workout', 'exercise']
        db_table = "workout_exercises"

    def save(self, *args, **kwargs):
        # mnually trigger the validators even if modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.id}"