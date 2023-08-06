from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import jwt
from django.conf import settings

class UserAPIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = self.get_token_from_request(request)
        if not token:
            return None
        
        return self.authenticate_token(token)


    def get_token_from_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        start_str = "Bearer"
        if auth_header and auth_header.startswith(f'{start_str} '):
            return auth_header.split(' ')[1] 

        return None

    def authenticate_token(self, token):
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(_('Token has expired'))
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed(_('Invalid access token provided'))

        user_id = decoded_token.get('user_id')

        if not user_id:
            raise exceptions.AuthenticationFailed(_('Invalid token'))
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('User not found'))
        return (user, None)