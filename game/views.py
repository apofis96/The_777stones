from django.shortcuts import render
from django.shortcuts import redirect
from .forms import NewGameForm
from .forms import JoinGameForm
from .forms import JoinPrivateGameForm
from testapp.models import Game
from django.http import  HttpResponseRedirect
from django import forms

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
    form = NewGameForm()
    return render(request,'game/newGame.html', {'form': form})

def joinGame(request):
    if request.method == "POST":
        if(request.session['firstJoin']):
            id = request.POST.get("id")
            games = Game.objects.get(pk=id)
            request.session['gameID'] = id
            if games.isPublic == False:
                request.session['gameAllow'] = False
                form = JoinPrivateGameForm()
                request.session['firstJoin'] = False
                return render(request, 'game/joinPrivateGame.html', {'form': form, 'kek': 2, 'games': games})
            else:
                request.session['gameAllow'] = True
                return HttpResponseRedirect ('play')
        else:
            games = Game.objects.get(pk=request.session['gameID'])
            name = request.POST.get("gameName")
            if name == games.gameName:
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

def joinPrivateGame(request, game):
    if request.method == "POST":
        name = request.POST.get("gameName")
        if name == game.gameName:
            return playGame(request, game)
        else:   return newGame(request)
    form = JoinPrivateGameForm()
    return render(request,'game/joinPrivateGame.html', {'form': form, 'kek' : 2, 'game' : game})

def playGame(request):
    if request.session['gameAllow']:
        game = Game.objects.get(pk=request.session['gameID'])
    return render(request,'game/playGame.html', {'games': game})