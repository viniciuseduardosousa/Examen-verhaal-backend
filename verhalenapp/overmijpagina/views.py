from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class Overmijview(APIView):

    def get(self,request):
        overmij = Overmij.objects.get()
        serializer = OvermijSerializer(overmij, many=False, context={'request': request})
        return Response(serializer.data)

class Footerview(APIView):
    
    def get(self,request):
        footer = Footer.objects.get()
        serializer = FooterSerializer(footer, many=False, context={'request': request})
        return Response(serializer.data)

class OvermijAdminview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        overmij = Overmij.objects.get()
        serializer = OvermijSerializer(overmij, many=False, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        overmij = Overmij.objects.get()
        serializer = OvermijSerializer(overmij, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request):
        overmij = Overmij.objects.get()
        serializer = OvermijSerializer(overmij, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class FooterAdminview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        footer = Footer.objects.get()
        serializer = FooterSerializer(footer, many=False, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        footer = Footer.objects.get()
        serializer = FooterSerializer(footer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request):
        footer = Footer.objects.get()
        serializer = FooterSerializer(footer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)