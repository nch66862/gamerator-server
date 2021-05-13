from django.db import models

class Game(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    designer = models.CharField(max_length=100)
    year_released = models.DateField(auto_now=False, auto_now_add=False)
    number_of_players = models.IntegerField()
    time_to_play = models.IntegerField()
    min_age_recommendation = models.IntegerField()
    categories = models.ManyToManyField("Category")
