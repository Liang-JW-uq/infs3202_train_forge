from django.db import models
from .tag import Tag
from .exercise import Exercise

class TagExercise(models.Model):
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
    
    def save(self, *args, **kwargs):
        # mnually trigger the validators when modelform not used
        self.full_clean() 
        super().save(*args, **kwargs)      

    def __str__(self):
        return self.name