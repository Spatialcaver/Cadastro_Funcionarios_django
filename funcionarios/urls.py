from django.urls import path
from .views import FuncionarioCreateView, FuncionarioListView, FuncionarioUpdateView, FuncionarioDeleteView

urlpatterns = [
    path('funcionarios/registrar/', FuncionarioCreateView.as_view()),
    path('funcionarios/listar/', FuncionarioListView.as_view()),
    path('funcionarios/atualizar/<int:pk>/', FuncionarioUpdateView.as_view()),
    path('funcionarios/deletar/<int:pk>/', FuncionarioDeleteView.as_view())
]
