from rest_framework import serializers
from .models import HangmanApi

class HangmanApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = HangmanApi
        fields = '__all__'
