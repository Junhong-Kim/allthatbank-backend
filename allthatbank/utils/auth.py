import jwt
from datetime import datetime, timedelta

from django.conf import settings


class Authentication:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY

    def create_token(self, user):
        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=3600),
            'user': {
                'id': user.id,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'email': user.email,
                'nickname': user.nickname,
                'picture_url': user.picture_url,
                'sns_type': user.sns_type,
                'sns_id': user.sns_id,
                'sns_access_token': user.sns_access_token,
                'role': user.role,
                'username': user.username
            }
        }
        token = jwt.encode(payload=payload, key=self.secret_key, algorithm='HS256')
        return token

    def validate_token(self, token, secret_key):
        try:
            data = jwt.decode(jwt=token, key=secret_key, algorithms='HS256')
            return data
        except jwt.ExpiredSignatureError:
            return '만료된 토큰'
        except jwt.InvalidTokenError:
            return '유효하지 않은 토큰'
