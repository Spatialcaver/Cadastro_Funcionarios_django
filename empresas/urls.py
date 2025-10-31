from django.contrib import admin
from .views import EmpresasCreateView, EmpresasListView, EmpresasUpdateView, EmpresasDeleteView
from django.urls import include, path

urlpatterns = [
    path('registrar/', EmpresasCreateView.as_view()), 
    path('listar/', EmpresasListView.as_view()), 
    path('atualizar/<int:pk>/', EmpresasUpdateView.as_view()),
    path('deletar/<int:pk>/', EmpresasDeleteView.as_view())
]