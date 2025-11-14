from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        fields = ('id', 'name', 'matricula', 'email', 'is_active', 'is_staff', 'is_superuser')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        # 🛑 CORREÇÃO: Adicione 'is_staff' nos campos
        fields = ('id', 'name', 'email', 'matricula', 'password', 'is_staff') 
        extra_kwargs = {
            # Torna is_staff opcional para ser usado se o Admin o fornecer.
            'is_staff': {'required': False} 
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        
        # 🛑 CORREÇÃO: Pop o is_staff também, com um default seguro (False)
        is_staff = validated_data.pop('is_staff', False) 
        
        user = User(**validated_data)
        user.set_password(password)
        
        # Define is_staff baseado no valor fornecido (apenas se for fornecido True)
        user.is_staff = is_staff 
        
        user.save()
        return user

