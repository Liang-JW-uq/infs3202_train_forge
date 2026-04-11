from django.db import models
from orm.models import UserTrainer
from orm.models import Client
from datetime import datetime, date
from django.core.exceptions import ValidationError  

class Appointment(models.Model):
    # setup apppointment buckets
    class PREFERRED_TIMES(models.TextChoices):
        MORNING = "Morning", "Morning"
        AFTERNOON = "Afternoon", "Afternoon"
        NIGHT = "Night", "Night"


    trainer = models.ForeignKey(
        UserTrainer,
        on_delete = models.CASCADE,
        related_name = "appointments"
    )
    client = models.ForeignKey(
        Client,
        on_delete = models.CASCADE,
        related_name = "appointments"
    )

    scheduled_date = models.DateField()
    scheduled_time = models.CharField(
        max_length=12,
        choices = PREFERRED_TIMES,
        default = PREFERRED_TIMES.MORNING
    )

    class Meta:
        # ????? workable to ensure no double booking ?????
        unique_together = ['trainer', 'scheduled_date', 'scheduled_time']
        db_table  = "appointments"

    
    def save(self, *args, **kwargs):
        # mnually trigger the validators when modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)

    # Date Checking to prevent dates in the past from being chosen (Validators don't have this specific checking)
    def clean(self):
        cleaned_data = super().clean()

        # this will check for inputs dates > current date, else raise error
        if self.scheduled_date < date.today():
            raise ValidationError({"scheduled_date": "Must be a future date. This is from the model!"})  
            # self.add_error("scheduled_date", "Must be a future date. This is from the model!")

        return cleaned_data

    def __str__(self):
        return f"Appointment"
    
    