from rest_framework import serializers
from verhalen.models import *

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'
    cover_image = serializers.ImageField(required=False)

class VerhaalSerializer(serializers.ModelSerializer):
    categorie = serializers.PrimaryKeyRelatedField(queryset=Categorie.objects.all())
    class Meta:
        model = Verhaal
        fields = '__all__'
    cover_image = serializers.ImageField(required=False)
