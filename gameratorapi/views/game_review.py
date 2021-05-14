"""View module for handling requests about pictures"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from gameratorapi.models import Player, Game, Review
from django.db.models import Count, Q


class GameReviewView(ViewSet):
    """Gamerator Games"""

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        reviews = Review.objects.all()

        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        #pk is pk of a game
        try:
            reviews = Review.objects.filter(game__id=pk)
            serializer = ReviewSerializer(reviews, context={'request': request}, many=True)
            return Response(serializer.data)
        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        # Get the current authenticated user
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["gameId"])

        review = Review()
        review.game = game
        review.player = player
        review.text = request.data["text"]
        review.rating = request.data["rating"]
        review.time_stamp = request.data["timeStamp"]

        try:
            review.save()
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    user = UserSerializer()

    class Meta:
        model = Player
        fields = ('id', 'user')

class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    player = PlayerSerializer()

    class Meta:
        model = Review
        fields = ('id', 'text', 'player', 'rating', 'game', 'time_stamp')
