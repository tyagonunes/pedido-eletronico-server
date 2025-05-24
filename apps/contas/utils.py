import requests
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from google.oauth2 import id_token
from google.auth.transport import requests


GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'



def generate_tokens_for_user(user):
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token


def google_get_user_info(access_token):
    try: 
        return id_token.verify_oauth2_token(
            access_token, 
            requests.Request(), 
            settings.GOOGLE_OAUTH2_CLIENT_ID
        )
    except Exception as e:
        return None


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default

def get_error_message(exc) -> str:
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        error_msg = ', '.join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg