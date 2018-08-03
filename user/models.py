from django.db import models


class User(models.Model):
    USER_ROLE = (
        ('A', 'Admin'),
        ('G', 'Guest')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.CharField(max_length=100, null=True)
    nickname = models.CharField(max_length=50, null=True)
    picture_url = models.CharField(max_length=255, null=True)
    sns_type = models.CharField(max_length=50, null=True)
    sns_id = models.CharField(max_length=255, null=True)
    sns_access_token = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLE, default='G')
    username = models.CharField(max_length=100, null=True, unique=True)
    password = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'users'
        unique_together = ('sns_type', 'sns_id')
