__author__ = 'grantpowell'

from django import forms


class MakeMoveForm(forms.Form):
    move = forms.IntegerField()
    game = forms.IntegerField()
    difficulty = forms.IntegerField(initial=1)