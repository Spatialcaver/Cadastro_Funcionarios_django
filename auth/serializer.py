from rest_framework import serializers
from django.conf import settings
from contas.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'avatar', 'is_superuser', 'last_access')
        read_only_fields = ('id', 'is_superuser', 'last_access')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = f"{settings.CURRENT_URL}{instance.avatar}" if data['avatar'] else None
        return data