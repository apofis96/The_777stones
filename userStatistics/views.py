from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from testapp.models import Game
from django.db.models import Q
from django.contrib.auth.models import User

# Create your views here.
@login_required()
def statsAll(request):

    currentUser = request.user;
    games=Game.objects.filter(Q(ownerID = currentUser) | Q(secondPlayerID = currentUser) )
    wonGames=games.filter(winnerID=currentUser)

    users = User.objects.all()

    rating = list()

    for u in users:
        games1 = Game.objects.filter(isCompleted=True).filter(Q(ownerID=u) | Q(secondPlayerID=u))
        wins = games.filter(winnerID=u).count()
        if games1.count() > 0:
            item = (u, wins / games1.count())
            rating.append(item)

    rating.sort(key=(lambda i: i[1]), reverse=True)

    for r in rating:
        if r[0] == currentUser:
            currUserPlace = rating.index(r) + 1


    return render(
        request,'stats/statsAll.html', { 'currentUser': { 'username': currentUser.get_username,
                                                          'place': currUserPlace,
                                                          'amountGamesPlayed': games.count(),
                                                          'victories': wonGames.count(),
                                                          'winrate': "{0:.2f}".format(
                                                              wonGames.count() * 100 / games.filter(
                                                                  isCompleted=True).count()),
                                                          },
                                         'bestUser': {'user': rating[0][0], 'winrate': "{0:.2f}".format(rating[0][1] * 100)},
                                         'worstUser': {'user': rating[-1][0], 'winrate': "{0:.2f}".format(rating[-1][1] * 100)}}
    )