# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    uname = models.CharField(max_length=20, null=True)
    # можливості для розширення..

class Game(models.Model):
    isCompleted = models.BooleanField(default=False)
    isPublic = models.BooleanField()
    password = models.CharField(max_length=10, null=True)
    gameName = models.CharField(max_length=100, default='NoNameGame')
    ownerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    secondPlayerID =models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='secondPlayer')
    winnerID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='winner')
    ownerScore = models.IntegerField(default=0)
    secondPlayerScore = models.IntegerField(default=0)
class GameMove(models.Model):
    gameID = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game')
    moveNo = models.IntegerField()
    # 'r' == rock(stone), 's' == scissors, 'p' == paper
    ownerMove = models.CharField(max_length=1, null=True)
    secondPlayerMove = models.CharField(max_length=1, null=True)


