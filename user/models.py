from django.db import models

from allthatbank.utils.auth import Authentication
from allthatbank.utils.cipher import AESCipher


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

    @staticmethod
    def authentication(username, password):
        user = User.objects.get(username=username)
        if password is None:
            decrypted_password = None
        else:
            decrypted_password = AESCipher().decrypt_str(user.password)

        if password == decrypted_password:
            token = Authentication().create_token(user)
            return token
        else:
            return None

    class Meta:
        db_table = 'users'
