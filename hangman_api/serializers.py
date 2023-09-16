from rest_framework import serializers
from .models import HangmanApi

class HangmanApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = HangmanApi
        fields = '__all__'


class GuessSerializer(serializers.Serializer):
    guessed_letter = serializers.CharField()

    def validate_guessed_letter(self, value):
        # Convert the guessed letter to lowercase before validation
        value = value.lower()
        
        if not value.isalpha() or len(value) != 1:
            raise serializers.ValidationError("Guessed letter must be a single alphabetical character.")
        
        return value