from rest_framework.serializers import ModelSerializer, SerializerMethodField
from apps.contas.models import *



class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return user