from django.contrib import admin

# Register your models here.
# contas/admin.py

from django.contrib import admin
# Importar seu modelo User customizado
from .models import User 
# Importar o Admin padrão do Django para o modelo User customizado
from django.contrib.auth.admin import UserAdmin 

# -----------------------------------------------------
# OPÇÃO 1: Usar o UserAdmin padrão do Django
# -----------------------------------------------------
# O UserAdmin é uma classe que fornece toda a funcionalidade de display, 
# edição e busca para gerenciar usuários no Admin.
class CustomUserAdmin(admin.ModelAdmin): # <--- NÃO HERDA DE UserAdmin
    list_display = ('email', 'name', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name')
    # Use fieldsets/add_fieldsets simples
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('name', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'name', 'password', 'is_staff', 'is_superuser')}),
    )
# -----------------------------------------------------
# 2. Registrar modelo User customizado no Admin
# -----------------------------------------------------
admin.site.register(User, CustomUserAdmin)