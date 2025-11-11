from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    matricula = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        matricula = attrs.get('matricula')
        password = attrs.get('password')

        try:
            user = User.objects.get(matricula=matricula)
        except User.DoesNotExist:
            raise serializers.ValidationError('Matrícula ou senha inválidas')

        if not user.check_password(password):
            raise serializers.ValidationError('Matrícula ou senha inválidas')

        if not user.is_active:
            raise serializers.ValidationError('Usuário inativo')

        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data

    @classmethod
    def get_token(cls, user):
        from rest_framework_simplejwt.tokens import RefreshToken
        return RefreshToken.for_user(user)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'matricula', 'email', 'is_active')

