# funcionarios/urls.py (Correção)

from django.urls import path
from .views import (
    FuncionarioListCreateView,
    FuncionarioRetrieveUpdateDestroyView,
    BaterPontoAPIView,
    ProgressoMetaView,
    MinhasJornadasView, 
    GestaoRankingView,
)

urlpatterns = [
    # Rotas de CRUD (Consolidado)
    path('', FuncionarioListCreateView.as_view(), name='funcionario-list-create'),
    path('<int:pk>/', FuncionarioRetrieveUpdateDestroyView.as_view(), name='funcionario-detail'),
    path('ponto/bater/', BaterPontoAPIView.as_view(), name='bater-ponto'),
    path('progresso/', ProgressoMetaView.as_view(), name='progresso-meta'),
    path('jornadas/me/', MinhasJornadasView.as_view(), name='minhas-jornadas'),
    path('controle/ranking/', GestaoRankingView.as_view(), name='controle-ranking'),
]