from rest_framework import serializers
from django.conf import settings
from contas.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name',  'is_superuser', 'last_access')
        read_only_fields = ('id', 'is_superuser', 'last_access')

   