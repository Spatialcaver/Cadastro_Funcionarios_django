from django.db import models
from django.forms import CharField

# Create your models here.
class Empresa(models.Model):
    razao_social = models.CharField(max_length=100, null=False, blank=False)
    cnpj = models.CharField(max_length=18, null=False, blank=False, unique=True)
    segmento = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return f'{self.razao_social}'
    
    

