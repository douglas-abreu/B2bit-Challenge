from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from django.conf import settings
from datetime import timedelta


def expires_in(token):
    """Token Expires In

    Return the left time to token expire
    """

    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time


def is_token_expired(token):
    """Is Token Expires

    Return the boolean if token is expired
    """

    return expires_in(token) < timedelta(seconds = 0)


def token_expire_handler(token):
    """Token Expire Handler

    If token is expired, then a new one will be created
    """

    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user = token.user)
    return is_expired, token


class ExpiringTokenAuthentication(TokenAuthentication):
    """Expiring Token Authentication

    If token is expired then it will be removed
    and new one with different key will be created
    """

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key = key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")
        
        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")

        is_expired, token = token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed("The Token is expired")
        
        return (token.user, token)