from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView






urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/v1/funcionarios/', include('funcionarios.urls')),
    path('core/v1/empresas/', include('empresas.urls')),
    path('core/v1/auth/', include('auth.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('auth/', include('auth.urls'))
]