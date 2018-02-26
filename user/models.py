from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=128)
    name = models.CharField(max_length=64)
    gender = models.CharField(max_length=32)
    birthday = models.CharField(max_length=32)
    picture = models.CharField(max_length=256)
    fb_access_token = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
