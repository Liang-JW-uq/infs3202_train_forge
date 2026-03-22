from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator, MinValueValidator
from .trainer import Trainer

class Tag(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="tags"
    )
    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(5)],
        unique=True
    )
    

    class Meta:
        db_table="tags"

    def __str__(self):
        return self.name