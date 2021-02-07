from rest_framework import serializers

from .models import Client, Gamer, GameQuestion


class GamerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gamer
        fields = ['name', 'points']

class GameQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Gamer
        fields = ['text']
