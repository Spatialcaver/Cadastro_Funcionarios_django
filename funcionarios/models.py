from django.db import models


# Create your models here.
class Funcionario(models.Model):
    nome = models.CharField(max_length = 100, null=False, blank=False)
    cpf = models.CharField(max_length=14,blank=False, unique=True)
    matricula = models.CharField(max_length=7, null=False, blank=False, unique=True)
    cargo = models.CharField(max_length= 30, null=False, blank=False)
    idade = models.IntegerField(null=False, blank=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['cpf', 'matricula']),
        ]

    def __str__(self):
            return f"{self.nome} - {self.matricula}"