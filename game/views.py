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
from userStatistics.views import notify , notifyDel


#class IDGameForm(forms.Form):
#    id = forms.IntegerField(label="ID")

# Create your views here.
def asideParams(user):
    activeGames = Game.objects.filter(Q(ownerID=user) | Q(secondPlayerID=user))
    activeGames = activeGames.exclude(isCompleted=True)
    return activeGames

@login_required()
def game(request):
    games = Game.objects.filter(Q(secondPlayerID__isnull=True), isCompleted=False)
    games = games.exclude(ownerID=request.user)
    activeGames = Game.objects.filter(Q(ownerID=request.user) | Q(secondPlayerID=request.user))
    activeGames = activeGames.exclude(isCompleted=True)
    return render(
        request, 'game/game.html', {'userGames': activeGames,
                                    'games': games,
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
            request.session.modified = True
            request.session['game'] = {}
            newGame = Game()
            newGame.gameName = request.POST.get('gameName')
            if(request.POST.get('gameType') == 'Private'):
                newGame.password = request.POST.get('password')
                newGame.isPublic = False
            else:
                newGame.isPublic = True
            newGame.ownerScore = 0
            newGame.secondPlayerScore = 0
            newGame.ownerID = request.user
            newGame.save()
            request.session.modified = True
            request.session['game']['gameID'] = newGame.pk
            #return HttpResponseRedirect('play')
            return redirect('Active Game')
    form = NewGameForm()
    return render(request,'game/newGame.html', {'form': form,
                                                'userGames': asideParams(request.user)})

@login_required()
def joinGame(request):
    id = request.GET.get("id")
    games = Game.objects.filter(isCompleted=False, pk=id)
    if games[0]:
        request.session.modified = True
        request.session['game'] = {}
        request.session['game']['gameID'] = id
        request.method = request.POST
        return redirect('Active Game')


@login_required()
def playGame(request):
    request.session.modified = True
    currGame = Game.objects.filter(pk=request.session['game']['gameID'])[0]
    global moves
    moves = GameMove.objects.filter(gameID=currGame.id).order_by('-moveNo')
    params = {'game': currGame,
              'userGames': asideParams(request.user),
        'moves' : moves,
        'isApproved' : currGame.secondPlayerID == None,
        'passwordRequired': currGame.isPublic == False and currGame.secondPlayerID == None,
        'wrongPassMessageOn': False}
    if (currGame.ownerID != request.user) and (currGame.secondPlayerID == None):
        if currGame.isPublic:
            currGame.secondPlayerID = request.user
            currGame.save()
        else:
            if request.POST.get('password') == currGame.password:
                currGame.secondPlayerID = request.user
                currGame.save()
                params['passwordRequired'] = False
            else:
                params['wrongPassMessageOn'] = True;
    else:
        if (currGame.secondPlayerID != request.user and  currGame.ownerID != request.user):
            return redirect('All Games')
        notifyDel(currGame, request.user)
        params['passwordRequired'] = False
        move = request.POST.get('move')
        if request.method == "POST" and move != 'e':
            if currGame.secondPlayerID == request.user:
                notify(currGame, currGame.ownerID, 'm')
                if moves.count() == 0 or (moves[0].secondPlayerMove is not None and moves[0].ownerMove is not None):
                    newMove = GameMove()
                    newMove.gameID = currGame
                    newMove.moveNo = moves.count()
                    newMove.secondPlayerMove = move
                    newMove.save()
                    #return HttpResponse("<h2>Kek</h2>")
                else:
                    #return HttpResponse("<h2>Kok</h2>")
                    lastMove = moves[0]
                    lastMove.secondPlayerMove = move
                    lastMove.save()
            elif currGame.ownerID == request.user:
                notify(currGame, currGame.secondPlayerID, 'm')
                if moves.count() == 0 or (moves[0].ownerMove is not None and moves[0].secondPlayerMove is not None):
                    #return HttpResponse("<h2>Kak</h2>")
                    newMove = GameMove()
                    newMove.gameID = currGame
                    newMove.moveNo = moves.count()
                    newMove.ownerMove = move
                    newMove.save()
                else:
                    lastMove = moves[0]
                   # return HttpResponse("<h2>Kuk</h2>")
                    lastMove.ownerMove = move
                    lastMove.save()
            else:
                return redirect('All Games')
            return HttpResponseRedirect('activeGame')
    owScore = 0; secScore = 0
    for move in moves:
        if move.ownerMove == 's':
            if move.secondPlayerMove == 'r':
                secScore += 1
            elif move.secondPlayerMove == 'p':
                owScore += 1
        elif move.ownerMove == 'p':
            if move.secondPlayerMove == 's':
                secScore += 1
            elif move.secondPlayerMove == 'r':
                owScore += 1
        elif move.ownerMove == 'r':
            if move.secondPlayerMove == 'p':
                secScore += 1
            elif move.secondPlayerMove == 's':
                owScore += 1
    currGame.ownerScore = owScore
    currGame.secondPlayerScore = secScore
    if moves[0].ownerMove is None or moves[0].secondPlayerMove is None:
        moves = moves[1:]

    move = request.POST.get('move')
    if move == 'e':
        if (request.user == currGame.ownerID):
            notify(currGame,currGame.secondPlayerID,'e')
        else:
            notify(currGame,currGame.ownerID,'e')

        if owScore > secScore:
            currGame.winnerID = currGame.ownerID
        elif owScore < secScore:
            currGame.winnerID = currGame.secondPlayerID
        currGame.isCompleted = True
        currGame.save()
        return game(request)
    currGame.save()
    params['isApproved'] = currGame.secondPlayerID != None
    params['moves'] = moves
    return render(request, 'game/activeGame.html', params)


@login_required()
def joinGame1(request):
    request.session.modified = True
    if(request.session['firstJoin']):
        id = request.GET.get("id")
        games = Game.objects.get(pk = id)
        if(games.secondPlayerID == None) or (games.secondPlayerID == request.user) or (games.ownerID == request.user):
            request.session['game']['gameID'] = id

            # для приватной
            if (games.isPublic == False) and (games.secondPlayerID == None):
                request.session['game']['gameAllow'] = False
                form = JoinPrivateGameForm()
                request.session['firstJoin'] = False
                request.session.modified = True
                return render(request, 'game/joinPrivateGame.html', {'form': form, 'kok': request.session['game']['gameAllow'], 'games': games})
            # для публичной
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
            return HttpResponseRedirect('new');

@login_required()
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

@login_required()
def playGame1(request):
    request.session.modified = True
    request.session['game']['moveID'] = -1
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



@login_required()
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