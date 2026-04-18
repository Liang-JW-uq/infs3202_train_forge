from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator, MinValueValidator
from .user_trainer import UserTrainer as Trainer 

class Tag(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="tags"
    )
    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(5)]
    )
    

    class Meta:
        unique_together = ['trainer', 'name']
        db_table="tags"

    def save(self, *args, **kwargs):
        # mnually trigger the validators when modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)        

    def __str__(self):
        return self.name