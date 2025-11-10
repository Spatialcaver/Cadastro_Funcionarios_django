# funcionarios/views.py

from .models import Funcionario
from .serializers import FuncionarioSerializer
from rest_framework import generics, permissions


# ----------------------------------------------------------------------
# 1. FuncionarioListCreateView (Rota: /api/funcionarios/)
# Cobre: GET (Lista) e POST (Criação)
# ----------------------------------------------------------------------
class FuncionarioListCreateView(generics.ListCreateAPIView):
    """
    Permite listar todos os funcionários e criar um novo funcionário.
    Requer autenticação (JWT Token).
    """
    # Define todos os objetos que a View deve operar.
    queryset = Funcionario.objects.all()
    
    # Define qual Serializer será usado para a entrada/saída de dados.
    serializer_class = FuncionarioSerializer
    
    # Prioridade P2: Garante que apenas usuários autenticados possam listar/criar.
    permission_classes = [permissions.IsAuthenticated] 

    # Se necessário, esta função pode ser sobrescrita para adicionar lógica pré-save.
    # def perform_create(self, serializer):
    #     serializer.save()
    

# ----------------------------------------------------------------------
# 2. FuncionarioRetrieveUpdateDestroyView (Rota: /api/funcionarios/<pk>/)
# Cobre: GET (Detalhe), PUT/PATCH (Atualização) e DELETE (Deleção)
# ----------------------------------------------------------------------
class FuncionarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permite visualizar os detalhes, atualizar ou deletar um funcionário específico.
    Requer autenticação (JWT Token).
    """
    # Define todos os objetos que a View deve operar.
    queryset = Funcionario.objects.all()
    
    # Define qual Serializer será usado.
    serializer_class = FuncionarioSerializer
    
    # Prioridade P2: Garante que apenas usuários autenticados possam modificar/deletar.
    permission_classes = [permissions.IsAuthenticated]