from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import GamerSerializer
from .models import Gamer

class GamersList(APIView):
    def get(self, request):
        gamers = Gamer.objects.all()
        data = GamerSerializer(gamers, many=True).data
        return Response(data)


    