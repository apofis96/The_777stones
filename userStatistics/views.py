from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from testapp.models import Game
from django.db.models import Q

# Create your views here.
@login_required()
def statsAll(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    currentUser = request.user;
    games=Game.objects.filter(Q(ownerID = currentUser) | Q(secondPlayerID = currentUser) )
    wonGames=games.filter(winnerID=currentUser)

    return render(
        request,'stats/statsAll.html', { 'user': currentUser,
                                         'amount': games.count(),
                                         'victories': wonGames.count(),
                                         'winrate': "{0:.2f}".format(wonGames.count() * 100 / games.filter(isCompleted=True).count())}
    )