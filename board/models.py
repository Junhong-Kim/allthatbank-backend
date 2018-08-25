from django.db import models

from core.models import TimeStampedModel
from user.models import User


class Post(TimeStampedModel):
    BOARD_CATEGORY = (
        ('N', 'Notice'),
        ('F', 'FreeBoard'),
        ('Q', 'Question'),
    )

    category = models.CharField(max_length=50, choices=BOARD_CATEGORY, default='F')
    title = models.CharField(max_length=100)
    contents = models.TextField()
    views = models.IntegerField()
    like = models.IntegerField()
    user = models.ForeignKey(User, db_constraint=True, on_delete=models.CASCADE)


class Comment(TimeStampedModel):
    contents = models.TextField()
    like = models.IntegerField()
    post = models.ForeignKey(Post, db_constraint=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_constraint=True, on_delete=models.CASCADE)
