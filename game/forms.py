from django import forms

from testapp.models import Game

class NewGameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('isPublic', 'gameName',)

class JoinGameForm(forms.Form):
    id = forms.IntegerField(label="ID")

class JoinPrivateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('gameName',)