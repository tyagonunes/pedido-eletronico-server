from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.contas.mixins import PublicApiMixin, ApiErrorsMixin
from apps.contas.utils import generate_tokens_for_user, google_get_user_info
from apps.contas.models import User
from apps.contas.api.serializers import UserSerializer
from apps.contas.choices import METODO_REGISTRO_GOOGLE


class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        credential = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        credential = validated_data.get('credential')
        user_data = google_get_user_info(access_token=credential)

       
                              
        try:
            user = User.objects.get(email=user_data['email'])
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access': str(access_token),
                'refresh': str(refresh_token)
            }
            
            return Response(response_data)
        except User.DoesNotExist:
            first_name = user_data.get('given_name', '')
            last_name = user_data.get('family_name', '')

            user = User.objects.create(
                username=user_data['email'],
                email=user_data['email'],
                first_name=first_name,
                last_name=last_name,
                metodo_registro=METODO_REGISTRO_GOOGLE,
                foto_rede_social=user_data['picture']
            )
         
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access': str(access_token),
                'refresh': str(refresh_token)
            }
            return Response(response_data)