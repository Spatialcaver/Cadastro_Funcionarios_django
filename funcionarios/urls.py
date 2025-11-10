# funcionarios/urls.py (Correção)

from django.urls import path
from .views import FuncionarioListCreateView, FuncionarioRetrieveUpdateDestroyView # <-- Usar APENAS as classes consolidadas

urlpatterns = [
    # Rotas de CRUD (Consolidado)
    path('', FuncionarioListCreateView.as_view(), name='funcionario-list-create'),
    path('<int:pk>/', FuncionarioRetrieveUpdateDestroyView.as_view(), name='funcionario-detail'),
]