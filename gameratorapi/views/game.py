"""View module for handling requests about pictures"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from gameratorapi.models import Player, Game
from django.db.models import Count, Q


class GameView(ViewSet):
    """Gamerator Games"""

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get the current authenticated user
        # player = Player.objects.get(user=request.auth.user)
        games = Game.objects.all()

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'year_released', 'number_of_players', 'time_to_play', 'min_age_recommendation')