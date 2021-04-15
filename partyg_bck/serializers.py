import random
from django.views.defaults import bad_request
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
import django

from .models import *


class GamerSerializer(serializers.HyperlinkedModelSerializer):
    game_token = serializers.IntegerField(source='game.token', required=True)

    class Meta:
        model = Gamer
        fields = ('id', 'name', 'points', 'game_token')

    def create(self, v_data):
        games = Game.objects.filter(token=v_data['game']['token'])
        theGame = next(game for game in games if game.active == True)
        # if not found TODO  #if both of them had been found TODO
        return Gamer.objects.create(game=theGame, name=v_data['name'])

    def update(self, instance, v_data):
        if instance.game.token != v_data['game']['token']:
            raise serializers.ValidationError("Game change is not allowed.")

        instance.name = v_data['name']
        instance.save()
        return instance


class GameSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.IntegerField(source="owner.id")
    token = serializers.ReadOnlyField()

    class Meta:
        model = Game
        fields = ['owner_id', 'num_of_rounds', 'current_round', 'active', 'token']

    def gen_8d_num(self):
        return random.randrange(1000000, 100000000 - 1, 1)

    def create(self, v_data):
        the_owner = Client.objects.get(pk=v_data['owner']['id'])
        # if the owner has a live game don't create a new one
        if the_owner.has_active_game():
            active_game = the_owner.active_game()
            active_game.num_of_rounds = v_data['num_of_rounds']
            active_game.save()
            return active_game

        return Game.objects.create(owner=the_owner,
                                   token=self.gen_8d_num(),
                                   num_of_rounds=v_data['num_of_rounds'],
                                   current_round=0)


class GamerQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GamerQuestion
        fields = ['text', 'subject_id', 'answered_by_all', 'voted_by_all']


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    publisher_id = serializers.IntegerField(source="publisher.id")
    game_token = serializers.IntegerField()

    class Meta:
        model = Answer
        fields = ['id', 'game_token', 'publisher_id', 'points', 'text']

    def validate(self, data):
        publisher = Gamer.objects.get(pk=data['publisher']['id'])
        if not publisher.game.active \
                or not (Game.objects.get(token=data['game_token']) == publisher.game):
            raise serializers.ValidationError("not allowed")
        return data

    def create(self, v_data):
        publisher = Gamer.objects.get(pk=v_data['publisher']['id'])
        question = publisher.game.get_current_question()
        text = v_data['text']
        ans, created = Answer.objects.get_or_create(
            gamer_question=question, publisher=publisher)
        # if created == False the answer already exists (new text:ignore or insert?)
        ans.text = text
        ans.save()
        return ans


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    voter_id = serializers.IntegerField(source="voter.id")
    selection_id = serializers.IntegerField(source="selection.id")

    class Meta:
        model = Vote
        fields = ['voter_id', 'selection_id']

    def validate(self, data):
        voter = Gamer.objects.get(pk=data['voter']['id'])
        selection = Answer.objects.get(pk=data['selection']['id'])

        if not voter.game.active\
           or not (selection.publisher.game == voter.game)\
           or voter == selection.publisher:
            raise serializers.ValidationError("not allowed")
        return data

    def create(self, v_data):
        voter = Gamer.objects.get(pk=v_data['voter']['id'])
        selection = Answer.objects.get(pk=v_data['selection']['id'])
        question = selection.gamer_question

        vote, created = Vote.objects.get_or_create(
            voter=voter, question=selection.gamer_question, selection=selection)
        # if created == False the answer already exists (new text:ignore or insert?)
        vote.selection = selection
        vote.save()
        question.finished = question.voted_by_all
        question.save()
        return vote
