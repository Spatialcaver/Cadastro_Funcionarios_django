from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView







urlpatterns = [
    path('admin/', admin.site.urls),
    path('funcionarios/', include('funcionarios.urls')),
    path('empresas/', include('empresas.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('auth/', include('contas.urls'))
]