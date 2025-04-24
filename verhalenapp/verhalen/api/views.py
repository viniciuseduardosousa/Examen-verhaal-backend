from django.shortcuts import render
from verhalen.models import *
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VerhalenList(APIView):

    def get(self,request):
        verhalen = Verhaal.objects.filter(is_onzichtbaar=False)
        serializer = VerhaalSerializer(verhalen, many=True, context={'request': request})
        return Response(serializer.data)
    
class CategorieList(APIView):
    def get(self,request):
        categorieen = Categorie.objects.all()
        serializer = CategorieSerializer(categorieen, many=True, context={'request': request})
        return Response(serializer.data)
    

class VerhalenDetail(APIView):
    def get_object(self, pk):
        try:
            return Verhaal.objects.get(pk=pk)
        except Verhaal.DoesNotExist:
            pass# raise Http404

    def get(self, request, pk):
        verhaal = self.get_object(pk)
        serializer = VerhaalSerializer(verhaal, context={'request': request})
        return Response(serializer.data)

class VerhalenListAdmin(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        verhalen = Verhaal.objects.all()
        serializer = VerhaalSerializer(verhalen, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer = VerhaalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerhalenDetailAdmin(APIView):
    def get_object(self, pk):
        try:
            return Verhaal.objects.get(pk=pk)
        except Verhaal.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        verhaal = self.get_object(pk)
        serializer = VerhaalSerializer(verhaal, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        verhaal = self.get_object(pk)
        serializer = VerhaalSerializer(verhaal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        verhaal = self.get_object(pk)
        verhaal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CategorieListAdmin(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        categorieen = Categorie.objects.all()
        serializer = CategorieSerializer(categorieen, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer = CategorieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategorieDetailAdmin(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Categorie.objects.get(pk=pk)
        except Categorie.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        categorie = self.get_object(pk)
        serializer = CategorieSerializer(categorie, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        categorie = self.get_object(pk)
        serializer = CategorieSerializer(categorie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        categorie = self.get_object(pk)
        categorie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    