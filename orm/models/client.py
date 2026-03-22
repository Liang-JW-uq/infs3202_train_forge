from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator, MinValueValidator
from .trainer import Trainer

class Client(models.Model):
    # This is a MANY sign : ForeignKey()
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="clients"
    )

    # trainer = Trainer.objects.filter(id=1)
    # clients = trainer.clients

    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5)]
    )
    age = models.IntegerField(
        db_default=0,
        validators=[MinValueValidator(18)]
    )
    email = models.CharField(
        max_length=50,
        validators= [EmailValidator()]
    )
    contact_no = models.CharField(
        max_length=20,
        validators = [MinLengthValidator(10)]
    )
    goals = models.TextField()
    preferred_times = models.CharField(
        max_length = 200
    )


    class Meta:
        unique_together = ['trainer', 'email'] # A client can register w/ multiple trainers, but cannot have duplicate emails per trainer

        db_table="clients"

    def __str__(self):
        return self.name