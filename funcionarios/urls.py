from django.urls import path
from .views import FuncionarioCreateView, FuncionarioListView, FuncionarioUpdateView, FuncionarioDeleteView

urlpatterns = [
    path('registrar/', FuncionarioCreateView.as_view()),
    path('listar/', FuncionarioListView.as_view()),
    path('atualizar/<int:pk>/', FuncionarioUpdateView.as_view()),
    path('deletar/<int:pk>/', FuncionarioDeleteView.as_view())
]
