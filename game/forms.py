from django import forms

from testapp.models import Game


class NewGameForm(forms.Form):

    gameName = forms.CharField(max_length=100)
    CHOICES = [('Public', 'Public'),
               ('Private', 'Private')]

    gameType = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), initial='Public')
    password = forms.CharField(max_length=100, min_length=10, required=False)

    if gameType == 'Private':
        password.required = True

class JoinGameForm(forms.Form):
    id = forms.IntegerField(label="ID")


class JoinPrivateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('gameName',)