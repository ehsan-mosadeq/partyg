from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

from .serializers import *
from .models import *

class GamersViewSet(
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   #mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = Gamer.objects.all().order_by('id')
    serializer_class = GamerSerializer
    #permission_classes = [IsAuthenticated]

class GamesViewSet(
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   #mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Game.objects.all().order_by('id')
    serializer_class = GameSerializer

from django.http import HttpResponseRedirect

def GLogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/accounts/google/login")


def MySocialLogin(request):
    print(request)
    return HttpResponse(request)