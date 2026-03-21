from django.db import models

class Trainer(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True
    )
    email = models.CharField(
        max_length=80
    )
    contact_no = models.CharField(
        max_length=20
    )

    # For testing purposes
    remarks = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    class Meta:
        db_table="trainers" # Must specify this otherwise by default they will put "<app name>_<model name>"

    def __str__(self):
        return self.name