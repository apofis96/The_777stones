from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import NewGameForm
from .forms import JoinGameForm
from .forms import JoinPrivateGameForm
from testapp.models import Game
from testapp.models import GameMove
from django.db.models import Q
from django.http import  HttpResponseRedirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User

#class IDGameForm(forms.Form):
#    id = forms.IntegerField(label="ID")

# Create your views here.
@login_required()
def game(request):
    games = Game.objects.filter(Q(secondPlayerID__isnull=True), isPublic=True, isCompleted=False)
    games = games.exclude(ownerID=request.user)
    return render(
        request, 'game/game.html', {'games': games,
                                    'allgamesstats': {
                                        'available': games.count(),
                                        'inProgress': Game.objects.filter(Q(secondPlayerID__isnull=False),
                                                                           isCompleted=False).count()
                                    }}
    )
@login_required()
def newGame(request):
    if request.method == "POST":
        form = NewGameForm(request.POST)
        if form.is_valid():
            newgame = form.save(commit=False)
            newgame.ownerID = request.user
            newgame.save()
    form = NewGameForm()
    return render(request,'game/newGame.html', {'form': form})

@login_required()
def joinGame(request):
    if request.method == "POST":
        if(request.session['firstJoin']):
            id = request.POST.get("id")
            games = Game.objects.get(pk=id)
            if(games.secondPlayerID == None) or (games.secondPlayerID == request.user) or (games.ownerID == request.user):
                request.session['gameID'] = id
                if games.isPublic == False:
                    request.session['gameAllow'] = False
                    form = JoinPrivateGameForm()
                    request.session['firstJoin'] = False
                    return render(request, 'game/joinPrivateGame.html', {'form': form, 'kek': 2, 'games': games})
                else:
                    request.session['gameAllow'] = True
                    if (games.secondPlayerID != request.user) and (games.ownerID != request.user):
                        games.secondPlayerID = request.user
                        games.save()
                    return HttpResponseRedirect ('play')
        else:
            games = Game.objects.get(pk=request.session['gameID'])
            name = request.POST.get("gameName")
            if name == games.gameName:
                if (games.secondPlayerID != request.user) and (games.ownerID != request.user):
                    games.secondPlayerID = request.user
                    games.save()
                request.session['gameAllow'] = True
                request.session['firstJoin'] = True
                return HttpResponseRedirect ('play')
            else:
                request.session['gameAllow'] = False
                return HttpResponseRedirect('new')
    form = JoinGameForm()
    request.session['gameAllow'] = False
    request.session['firstJoin'] = True
    return render(request,'game/joinGame.html', {'form': form, 'kek' : 1})

@login_required()
def joinPrivateGame(request, game):
    if request.method == "POST":
        name = request.POST.get("gameName")
        if name == game.gameName:
            return playGame(request, game)
        else:   return newGame(request)
    form = JoinPrivateGameForm()
    return render(request,'game/joinPrivateGame.html', {'form': form, 'kek' : 2, 'game' : game})

@login_required()
def playGame(request):
    if request.session['gameAllow']:
        games = Game.objects.get(pk=request.session['gameID'])
        IsNon = not games.isCompleted
        if (games.ownerScore == games.secondPlayerScore):
            IsPlay = False
        else: IsPlay = True
        game = {'IsNonCompleted' : IsNon, 'IsPlay': IsPlay}
        if request.method == "POST":
            if "newMove" in request.POST:
                try:
                    gameMov = GameMove.objects.order_by("-moveNo").filter(gameID=request.session['gameID'])[:1].first()
                except GameMove.DoesNotExist:
                    gameMov = GameMove()
                    gameMov.moveNo = 0
                    gameMov.gameID = games
                    gameMov.save()
                if (gameMov.ownerMove != None) and (gameMov.secondPlayerMove != None):
                    gameMovNew = GameMove()
                    gameMovNew.moveNo = (gameMov.moveNo + 1)
                    gameMovNew.gameID = games
                    gameMovNew.save()
                    gameMov = gameMovNew
                return HttpResponse("<h2>"+str(gameMov.moveNo)+"</h2>")
            elif "done" in request.POST:
                if IsPlay:
                    gameMov = GameMove.objects.order_by("-moveNo").filter(gameID=request.session['gameID'])[:1].first()
                    if (games.ownerScore > games.secondPlayerScore):
                        games.winnerID_id = games.ownerID_id
                    else: games.winnerID_id = games.secondPlayerID
                    if (gameMov.ownerMove == None) or (gameMov.secondPlayerMove == None):
                        gameMov.delete()
                    games.isCompleted = True
                    games.save()
                return HttpResponse("kek")
                return HttpResponse("<h2>Done</h2>")
        return render(request,'game/playGame.html', {'games': games, 'game' : game})
    return HttpResponse ("<h1>KekLOH</h1>")

@login_required()
def playMove (request):
    5