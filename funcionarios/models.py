from datetime import timedelta, timezone
from django.utils import timezone
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




class Jornada(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='jornadas')
    hora_entrada = models.DateTimeField(default=timezone.now)
    hora_saida = models.DateTimeField(blank=True, null=True)
    horas_trabalhadas = models.DecimalField(max_digits = 5, decimal_places=2, default=0.00)
    
    
    class Meta:
        verbose_name ="Jornada de Trabalho"
        ordering =['-horas_trabalhadas']  
        
    def calcular_horas_trabalhadas(self):
        if self.hora_entrada and self.hora_saida:
            duracao: timedelta = self.hora_saida - self.hora_entrada
            return round(duracao.total_seconds() / 3600, 2) 
        return 0.00
    
    def save(self, *args, **kwargs):
        # Garante que as horas trabalhadas sejam calculadas antes de salvar
        self.horas_trabalhadas = self.calcular_horas_trabalhadas()
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        saida = self.hora_saida.strftime('%H:%M') if self.hora_saida else 'EM ANDAMENTO'
        return f"{self.funcionario.usuario.name} | Entrada: {self.hora_entrada.strftime('%Y-%m-%d')} | Saída: {saida}" if self.hora_entrada else 'Hora de entrada não registrada'