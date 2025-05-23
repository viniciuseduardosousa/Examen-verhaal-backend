from rest_framework import serializers
from .models import *

class OvermijSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overmij
        fields = '__all__'
    afbeelding = serializers.ImageField(required=False)

class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = '__all__'