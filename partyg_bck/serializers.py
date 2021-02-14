import random
from rest_framework import serializers

from .models import *


class GamerSerializer(serializers.HyperlinkedModelSerializer):
    game_token = serializers.IntegerField(source='game.token', required=True)

    class Meta:
        model = Gamer
        fields =('id', 'name', 'points', 'game_token')

    def create(self, v_data):
        games = Game.objects.filter(token=v_data['game']['token'])
        theGame = next(game for game in games if game.active == True)
        #if not found TODO  #if two of them had been found TODO

        return Gamer.objects.create(game=theGame, name = v_data['name'])

    def update(self, instance, v_data):
        if instance.game.token != v_data['game']['token']:
            raise serializers.ValidationError("Game change is not allowed.")

        instance.name = v_data['name']
        instance.save()
        return instance

class GameSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.IntegerField(source = "owner.id")
    token = serializers.ReadOnlyField()

    class Meta:
        model = Game
        fields =['owner_id', 'num_of_rounds', 'active', 'token']

    def gen_8d_num(self):
        return random.randrange(1000000, 100000000 - 1, 1)

    def create(self, v_data):
        theOwner = Client.objects.get(pk = v_data['owner']['id'])
        # TODO if not found
        return Game.objects.create(owner = theOwner,
                                   token = self.gen_8d_num(),
                                   num_of_rounds = v_data['num_of_rounds'],
                                   current_round = 0)


# class GameQuestionSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Gamer
#         fields = ['text']
