from rest_framework.views import APIView
from .models import Empresa
from rest_framework.response import Response
from .serializer import EmpresaSerializer
from rest_framework import status

# Create your views here.
class EmpresasCreateView(APIView):
    def post(self, request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmpresasListView(APIView):
    def get(self, request):
        empresas = Empresa.objects.all()
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)
    
    
class EmpresasUpdateView(APIView):
    def put(self, request, pk):
        queryset = Empresa.objects.get(pk=pk)
        serializer = EmpresaSerializer(instance=queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class EmpresasDeleteView(APIView):
    def delete(self, request, pk):
        queryset = Empresa.objects.get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)