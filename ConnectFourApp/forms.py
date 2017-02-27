__author__ = 'grantpowell'

from django import forms


class MakeMoveForm(forms.Form):
    # Forms that inherit from the django form class come with CSRF validation and other neat stuff
    move = forms.IntegerField()
    game = forms.IntegerField()
    difficulty = forms.IntegerField(initial=1)