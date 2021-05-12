from django.db import models

class Review(models.Model):

    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    rating = models.IntegerField(max=5, min=1)
    time_stamp = models.DateTimeField(auto_now=False, auto_now_add=False)