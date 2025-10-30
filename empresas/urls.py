from django.contrib import admin
from .views import EmpresasCreateView, EmpresasListView, EmpresasUpdateView, EmpresasDeleteView
from django.urls import include, path

urlpatterns = [
    path('empresas/registrar/', EmpresasCreateView.as_view()), 
    path('empresas/listar/', EmpresasListView.as_view()), 
    path('empresas/atualizar/<int:pk>/', EmpresasUpdateView.as_view()),
    path('empresas/deletar/<int:pk>/', EmpresasDeleteView.as_view())
]