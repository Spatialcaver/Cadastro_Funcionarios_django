from django.db import models
from contas.models import User

class Funcionario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarios')
    cpf = models.CharField(max_length=14,blank=False, unique=True)
    matricula = models.CharField(max_length=7, null=False, blank=False, unique=True)
    cargo = models.CharField(max_length= 30, null=False, blank=False)
    idade = models.IntegerField(null=False, blank=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['cpf', 'matricula']),
        ]

    empresa = models.ForeignKey(
        'empresas.Empresa', on_delete=models.CASCADE,
        related_name='Funcionarios', 
        verbose_name='Empresa Contratante '
        )
    
    def __str__(self):
        return f"{self.usuario.name} - {self.matricula} - {self.empresa.razao_social}"


