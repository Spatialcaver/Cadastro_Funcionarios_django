# contas/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from contas.views import CustomTokenObtainPairView, SignInView, SignOutView, UserView 
from rest_framework_simplejwt.views import TokenObtainPairView 


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('me/', UserView.as_view(), name='profile_view')
]