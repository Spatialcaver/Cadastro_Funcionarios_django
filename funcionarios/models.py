from django.db import models


# Create your models here.
class Funcionario(models.Model):
    nome = models.CharField(max_length = 100)
    matricula = models.IntegerField()
    cargo = models.CharField(max_length= 30)
    idade = models.IntegerField()
    
    def __str__(self):
        return f"{self.matricula} - {self.nome} ({self.cargo}) Criado!"