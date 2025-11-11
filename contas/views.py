from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework import status
from contas.exeptions import ValidationError
from contas.serializer import CustomTokenObtainPairSerializer, UserSerializer
from contas.models import User
from django.conf import settings
from funcionarios.models import Funcionario
import uuid
import os
from contas.auth import AuthenticationService
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

User = get_user_model()


class SignInView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        matricula = request.data.get("matricula")
        password = request.data.get("password")

        auth_service = AuthenticationService()
        signin = auth_service.signin(matricula, password)

        if not signin:
            raise AuthenticationFailed(
                "Credenciais inválidas.", code=status.HTTP_401_UNAUTHORIZED
            )

        user = UserSerializer(signin).data
        refresh = RefreshToken.for_user(signin)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class SignUpView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not name or not email or not password:
            raise ValidationError(
                "Todos os campos são obrigatórios.", code=status.HTTP_400_BAD_REQUEST
            )

        auth_service = AuthenticationService()
        signup = auth_service.signup(name, email, password)

        if not signup:
            raise AuthenticationFailed(
                "Erro ao registrar.", code=status.HTTP_400_BAD_REQUEST
            )

        user = UserSerializer(signup).data
        refresh = RefreshToken.for_user(signup)

        return Response(
            {
                "result": {
                    "user": user,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            },
            status=status.HTTP_200_OK,
        )


class SignOutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        refresh_token = request.data.get("refresh")
        user = request.user
        

        if not refresh_token:
            raise AuthenticationFailed(
                "Token de atualização não fornecido.", code=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            user.last_access = now()
            user.save()
            token.blacklist()
        except TokenError:
            raise AuthenticationFailed(
                "Erro ao invalidar o token.", code=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            status=status.HTTP_205_RESET_CONTENT
        )


class UserView(APIView):

    def get(self, request):
        user = request.user

        User.objects.filter(id=user.id).update(last_access=now())

        if not user:
            raise AuthenticationFailed(
                "Usuário não autenticado.", code=status.HTTP_401_UNAUTHORIZED
            )

        user_data = UserSerializer(user).data

        return Response({"result": user_data}, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user

        if not user:
            raise AuthenticationFailed(
                "Usuário não autenticado.", code=status.HTTP_401_UNAUTHORIZED
            )

        name = request.data.get("name", user.name)
        email = request.data.get("email", user.email)
        password = request.data.get("password")
       

        user.name = name
        user.email = email
        
        if password:
            user.set_password(password)

        

        

        user.save()

        user_data = UserSerializer(user).data

        return Response({"result": user_data}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
            token = OutstandingToken.objects.get(token=request.auth)
            BlacklistedToken.objects.create(token=token)
            return Response({'detail': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)