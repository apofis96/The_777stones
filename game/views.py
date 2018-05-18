from django.shortcuts import render
from django.shortcuts import redirect
from .forms import NewGameForm
from .forms import JoinGameForm
from .forms import JoinPrivateGameForm
from testapp.models import Game
from testapp.models import GameMove
from django.http import  HttpResponseRedirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User

#class IDGameForm(forms.Form):
#    id = forms.IntegerField(label="ID")

# Create your views here.
def game(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,'game/game.html',
    )
def newGame(request):
    if request.method == "POST":
        form = NewGameForm(request.POST)
        if form.is_valid():
            newgame = form.save(commit=False)
            newgame.ownerID = request.user
            newgame.save()
            request.session.modified = True
            request.session['game'] = {}
            request.session['game']['gameAllow'] = True
            request.session['game']['gameID'] = newgame.pk
            return HttpResponseRedirect('play')
    form = NewGameForm()
    return render(request,'game/newGame.html', {'form': form})

def joinGame(request):
    if request.method == "POST":
        request.session.modified = True
        if(request.session['firstJoin']):
            id = request.POST.get("id")
            games = Game.objects.get(pk=id)
            if(games.secondPlayerID == None) or (games.secondPlayerID == request.user) or (games.ownerID == request.user):
                request.session['game']['gameID'] = id
                if (games.isPublic == False) and (games.secondPlayerID == None):
                    request.session['game']['gameAllow'] = False
                    form = JoinPrivateGameForm()
                    request.session['firstJoin'] = False
                    request.session.modified = True
                    return render(request, 'game/joinPrivateGame.html', {'form': form, 'kok': request.session['game']['gameAllow'], 'games': games})
                else:
                    request.session['game']['gameAllow'] = True
                    if (games.secondPlayerID != request.user) and (games.ownerID != request.user):
                        games.secondPlayerID = request.user
                        games.save()
                    request.session['firstJoin'] = False
                    return HttpResponseRedirect ('play')
        else:
            games = Game.objects.get(pk=request.session['game']['gameID'])
            name = request.POST.get("gameName")
            if name == games.gameName:
                if (games.secondPlayerID != request.user) and (games.ownerID != request.user):
                    games.secondPlayerID = request.user
                    games.save()
                request.session['game']['gameAllow'] = True
                request.session['firstJoin'] = True
                return HttpResponseRedirect ('play')
            else:
                request.session['game']['gameAllow'] = False
                return HttpResponseRedirect('new')
    form = JoinGameForm()
    request.session.modified = True
    request.session['game'] = {}
    request.session['game']['gameAllow'] = False
    request.session['firstJoin'] = True
    return render(request,'game/joinGame.html', {'form': form, 'kek' : 1})

#UNUSED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def joinPrivateGame(request, game):
    return HttpResponse("kek")
    request.session.modified = True
    if request.method == "POST":
        name = request.POST.get("gameName")
        if name == game.gameName:
            return playGame(request, game)
        else:   return newGame(request)
    form = JoinPrivateGameForm()
    return render(request,'game/joinPrivateGame.html', {'form': form, 'kok' : request.session['game']['gameAllow'], 'game' : game})

def playGame(request):
    request.session.modified = True
    request.session['game']['moveID'] = -1
    if (request.session['game']['gameAllow'] == True):
        games = Game.objects.get(pk=request.session['game']['gameID'])
        IsNon = not games.isCompleted
        if (games.ownerScore == games.secondPlayerScore):
            IsPlay = False
        else: IsPlay = True
        game = {'IsNonCompleted' : IsNon, 'IsPlay': IsPlay}
        if request.method == "POST":
            if "newMove" in request.POST:
                gameMov = GameMove.objects.order_by("-moveNo").filter(gameID=request.session['game']['gameID'])[:1].first()
                if(gameMov == None):
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
                request.session['game']['moveID'] = gameMov.pk
                return HttpResponseRedirect('playMove')
                #return HttpResponse("<h2>"+str(gameMov.moveNo)+"</h2>")
                #return playMove(request, gameMov, games)
            elif "done" in request.POST:
                if IsPlay:
                    gameMov = GameMove.objects.order_by("-moveNo").filter(gameID=request.session['game']['gameID'])[:1].first()
                    if (games.ownerScore > games.secondPlayerScore):
                        games.winnerID_id = games.ownerID_id
                    else: games.winnerID_id = games.secondPlayerID
                    if (gameMov.ownerMove == None) or (gameMov.secondPlayerMove == None):
                        gameMov.delete()
                    games.isCompleted = True
                    games.save()
                return HttpResponse("kek")
                return HttpResponse("<h2>Done</h2>")
        return render(request,'game/playGame.html', {'games': games, 'game' : game , 'kek' : request.session['game']['gameAllow'] })
    return HttpResponse ("<h1>KekLOH</h1>")

def playMove (request):
    try:
        request.session.modified = True
        if (request.session['game']['moveID'] == -1):
            return HttpResponseRedirect('play')
        change = False
        moveOld = ""
        oldMove = ""
        game = Game.objects.get(pk=request.session['game']['gameID'])
        gameMove = GameMove.objects.get(pk=request.session['game']['moveID'])
        if (request.user == game.ownerID):
            if (gameMove.ownerMove != None):
                change = True
                moveOld = gameMove.ownerMove
        elif (request.user == game.secondPlayerID):
            if (gameMove.secondPlayerMove != None):
                change = True
                moveOld = gameMove.secondPlayerMove
        else:
            del request.session['game']
            return HttpResponseRedirect('/')
        if (change):
                if ( moveOld == "s"):
                    oldMove = "Ножницы"
                elif ( moveOld == "r"):
                    oldMove = "Камень"
                elif ( moveOld == "p"):
                    oldMove = "Бумага"

        if request.method == "POST":
            del request.session['game']['moveID']
            if "stone" in request.POST:
                move = "r"
            if "paper" in request.POST:
                move = "p"
            if "scissors" in request.POST:
                move = "s"
            if (request.user == game.ownerID):
                gameMove.ownerMove = move
                gameMove.save()
                return HttpResponseRedirect('play')
            elif (request.user == game.secondPlayerID):
                gameMove.secondPlayerMove = move
                gameMove.save()
                return HttpResponseRedirect('play')
            del request.session['game']
            return HttpResponseRedirect('/')
            #return render(request, 'game/playMove.html')
        return render(request,'game/playMove.html', {'game' : game, 'change' : change, 'oldMove' : oldMove} )
    except KeyError:
        return HttpResponseRedirect("/")
    #return HttpResponse("kek")