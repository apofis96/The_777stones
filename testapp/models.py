from django.db import models

# Create your models here.
from django.db import models


class Players(models.Model):
    username = models.CharField(max_length=20)
    # можливості для розширення..

class Games(models.Model):
    isCompleted = models.BooleanField()
    isPublic = models.BooleanField()
    OwnerID = models.IntegerField()
    secondPlayerID = models.IntegerField()
    winnerID = models.IntegerField()

class GameMoves(models.Model):
    gameID = models.IntegerField()
    moveNo = models.IntegerField()
    # 'r' == rock(stone), 's' == scissors, 'p' == paper
    ownerMove = models.CharField(max_length=1)
    secondPlayerMove = models.CharField(max_length=1)


