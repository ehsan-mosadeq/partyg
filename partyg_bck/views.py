from django.http import HttpResponse
from django.http import HttpResponseRedirect
from rest_framework import viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .models import *


class GamersViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    serializer_class = GamerSerializer

    def get_queryset(self):
        game_token = self.request.query_params.get('GTKN')
        gamers = [gmr for gmr in Gamer.objects.all() if str(gmr.token()) == game_token]
        return gamers

class AnswerersViewSet(
    #mixins.CreateModelMixin,
    #mixins.RetrieveModelMixin,
    #mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    serializer_class = GamerSerializer

    def get_queryset(self):
        game_token = self.request.query_params.get('GTKN')
        game = Game.objects.all().filter(token=game_token)[0]
        gamers = game.get_current_answerers()
        return gamers


class VotersViewSet(
    #mixins.CreateModelMixin,
    #mixins.RetrieveModelMixin,
    #mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    serializer_class = GamerSerializer

    def get_queryset(self):
        game_token = self.request.query_params.get('GTKN')
        game = Game.objects.all().filter(token=game_token)[0]
        gamers = game.get_current_voters()
        return gamers


class GamesViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    serializer_class = GameSerializer

    def get_queryset(self):
        game_token = self.request.query_params.get('GTKN')
        gms = Game.objects.all().filter(token=game_token)
        return gms


def GLogin(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/google/login")

    registered_as_client = len(Client.objects.filter(pk=request.user.id).all()) > 0
    if not registered_as_client:
        usr = User.objects.get(pk=request.user.id)
        clt = Client(user_ptr_id=usr.id)
        clt.__dict__.update(usr.__dict__)
        clt.first_name = usr.username
        clt.mob_num = random.randrange(1000000, 100000000 - 1, 1)
        clt.save()

    clt = Client.objects.get(pk=request.user.id)
    if not clt.has_active_game():
        gen_8d_num = lambda: random.randrange(1000000, 100000000 - 1, 1)
        game = Game.objects.create(owner=clt,
                                   token=gen_8d_num(),
                                   num_of_rounds=10,
                                   current_round=0)
        game.save()

    game_token = clt.active_game().token
    auth_token = Token.objects.get_or_create(user=request.user)
    # TODO a game rounds page should be created
    response = HttpResponseRedirect("http://127.0.0.1:8080/start?GTKN={}&OWID={}".format(str(game_token), str(clt.id)))
    response['auth_token'] = auth_token
    return response


class GamerQuestionViewSet(
    # mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    serializer_class = GamerQuestionSerializer

    def get_queryset(self):
        game_token = self.request.query_params.get('GTKN')
        game = Game.objects.get(token=game_token)
        return [game.get_current_question()]

    def retrieve(self, request, pk=None):
        game = Game.objects.get(token=pk)
        serializer = self.serializer_class(game.get_current_question())
        return Response(serializer.data)


class WaitingViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    serializer_class = WaitingSerializer

    def get_queryset(self):
        game_token = self.request.query_params.get('GTKN')
        game = Game.objects.get(token=game_token)
        return game.gamers.all()


class AnswerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        game_token = self.request.query_params.get('GTKN')

        if game_token is None:
            return []

        game = Game.objects.get(token=game_token)

        return [ans for ans in game.get_current_question().answers_to_me.all()]


class VoteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):

    serializer_class = VoteSerializer

    def get_queryset(self):
        if not django.conf.settings.DEBUG:    # for debug
            return []

        ans_id = self.request.query_params.get('ANSID')
        if ans_id is None:
            return []

        ans = Answer.objects.get(pk=ans_id)
        return [vote for vote in ans.votes]
