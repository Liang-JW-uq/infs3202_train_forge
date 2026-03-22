from django.db import models
from .trainer import Trainer
from .client import Client

class Workout(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="workouts"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="workouts"
    )
    scheduled_time = models.DateTimeField()
    trainer_review_notes = models.TextField()
    client_remarks = models.TextField()
    is_completed = models.BooleanField(
        db_default=False
    )


    class Meta:
        db_table="workouts"

    def __str__(self):
        return self.name