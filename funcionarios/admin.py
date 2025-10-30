from django.contrib import admin
from .models import Funcionario

# Register your models here.


class AdminFuncionario(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'cargo', 'empresa', 'empresa__cnpj')
    search_fields = ('nome', 'cpf', 'cargo', 'empresa__razao_social', 'empresa__cnpj')
    
    
admin.site.register(Funcionario, AdminFuncionario)