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
    views = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    user = models.ForeignKey(User, db_constraint=True, on_delete=models.CASCADE)


class PostLike(TimeStampedModel):
    post = models.ForeignKey(Post, db_constraint=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_constraint=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'board_post_like'
        unique_together = ('post', 'user')


class Comment(TimeStampedModel):
    contents = models.TextField()
    like = models.IntegerField(default=0)
    post = models.ForeignKey(Post, db_constraint=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_constraint=True, on_delete=models.CASCADE)


class CommentLike(TimeStampedModel):
    comment = models.ForeignKey(Comment, db_constraint=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_constraint=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'board_comment_like'
        unique_together = ('comment', 'user')
