from rest_framework import serializers
from django.contrib.auth.models import User

from structure.models import Org

class OrgSerializerRestricted(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "description")
        model = Org

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "description", "password")
        model = Org


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
