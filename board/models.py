from django.db import models

from core.models import TimeStampedModel
from user.models import User


class Free(TimeStampedModel):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    views = models.IntegerField()
    like = models.IntegerField()
    user = models.ForeignKey(User, db_constraint=True, on_delete=models.CASCADE)
