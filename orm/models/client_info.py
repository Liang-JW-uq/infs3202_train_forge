from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator, MinValueValidator
from .client import Client
from .trainer import Trainer

class ClientInfo(models.Model):
    # This is specifically for ONE-TO-ONE relationships
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="clients_info"
    )
    identification_number = models.CharField(
        max_length=25
    )


    class Meta:
        db_table="clients_info"

    def __str__(self):
        return self.identification_number