# contas/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
# Importar APENAS as views necessárias e que você mantém
from .views import SignInView, SignOutView, UserView # <-- Assumindo que UserView lida com /me/# Nota: SignUpView foi removida. O login customizado será feito na SignInView, não mais na CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView # Usamos o padrão, e adaptamos o serializer.


urlpatterns = [
    # 1. Login (Usando a sua View customizada para tratar matrícula/senha)
    path('token/', SignInView.as_view(), name='token_obtain_pair'),
    
    # 2. Refresh de Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 3. Logout (Invalidação do Token)
    path('logout/', SignOutView.as_view(), name='logout'),
    
    # 4. Perfil do Funcionário Logado (GET e PATCH /me/)
    path('me/', UserView.as_view(), name='profile_view'),
    
    # Rota 'signin' e 'signup' REMOVIDAS para evitar duplicação e aderir à regra de negócio.
]