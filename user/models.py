from django.db import models


class User(models.Model):
    USER_ROLE = (
        ('A', 'Admin'),
        ('G', 'Guest')
    )

    email = models.EmailField(max_length=128, unique=True)
    name = models.CharField(max_length=64)
    gender = models.CharField(max_length=32)
    birthday = models.CharField(max_length=32)
    picture = models.CharField(max_length=256)
    fb_access_token = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=32, choices=USER_ROLE, default='G')

    class Meta:
        db_table = 'users'
