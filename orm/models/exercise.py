from django.db import models
from .trainer import Trainer

class Exercise(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="exercises"
    )
    name = models.CharField(
        max_length=30
    )
    instructions = models.TextField()
    default_sets = models.IntegerField(
        db_default=0
    )
    default_reps = models.IntegerField(
        db_default=0
    )
    default_weights = models.IntegerField(
        db_default=0
    )
    default_duration = models.IntegerField(
        db_default=0
    )

    class Meta:
        db_table="exercises"

    def __str__(self):
        return self.name