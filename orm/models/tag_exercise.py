from django.db import models
from .tag import Tag
from .exercise import Exercise

class TagExercise(models.Model):
    name = models.CharField(
        max_length=30
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="tags_exercises" # 
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="exercises_tags" # 
    )

    # # If we need ALL the exercises related to a tag...
    # tag = Tag.objects.filter(id=1)
    # exercises = tag.tag_exercises


    class Meta:
        db_table="tags_exercises"

    def __str__(self):
        return self.name