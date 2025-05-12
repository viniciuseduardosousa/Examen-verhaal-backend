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
    cover_image = serializers.ImageField(allow_null=True, required=False)

    # def update(self, instance, validated_data):
    #     if 'cover_image' in validated_data:
    #         if validated_data['cover_image'] is None:
    #             instance.cover_image.delete(save=False)
    #             instance.cover_image = None
    #         else:
    #             instance.cover_image = validated_data['cover_image']
    #     instance.save()
    #     return instance
