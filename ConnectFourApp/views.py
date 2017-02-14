# Django View Functions
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, RedirectView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth.mixins import LoginRequiredMixin

# models
from django.contrib.auth.models import User
from .models import Game, GameBoard

# forms
from django import forms
from .forms import MakeMoveForm

# Alpha Connect 4
from .alphaconnectfour import ai_simple_move

# other imports
import json

# Game Views

class HomePage(LoginRequiredMixin, ListView):
    template_name = 'exts/home_page.html'
    login_url = '/login/'
    ordering = ('gameboard.winner', 'starttime' )
    def get_queryset(self):
        return Game.objects.filter(user=self.request.user).all()

@login_required(login_url='/login/')
def gameview(request, game_pk=-1):
    ctext = dict()
    ctext['game'] = Game.objects.filter(user=request.user, pk=game_pk).first()
    ctext['gameswon'] = Game.objects.filter(user=request.user).filter(gameboard__winner=1).count()
    ctext['gameslost'] = Game.objects.filter(user=request.user).filter(gameboard__winner=2).count()
    ctext['gamesinprogress'] = Game.objects.filter(user=request.user).filter(gameboard__winner=0).count()

    if not ctext['game']:
        game = make_new_game_object(request.user, request.GET.get('difficulty',0))
        return HttpResponseRedirect('/gameview/{}'.format(game.id))

    return render(request, 'exts/game_view.html', context=ctext)


# Ajax Views


@login_required(login_url='/login/')
def gamedata(request, gamenum=-1):
    response_data = dict()
    player = 1
    cpu_player = 2

    if request.method == 'GET':
        # get the object from the database or make a new one
        gameobj = Game.objects.filter(pk=gamenum, user=request.user).first() or make_new_game_object(request.user, 0)
        response_data['cpu_move'] = -1

    if request.method == 'POST':

        # get and validate the csrf token and post values
        form = MakeMoveForm(request.POST)
        if not form.is_valid():
            return JsonResponse({'status': 'error', 'error_msg': 'form invalid'})
        move = form.cleaned_data['move']
        game = form.cleaned_data['game']

        # get the game object from the database
        gameobj = Game.objects.filter(pk=game, user=request.user).first()
        if not gameobj:
            return JsonResponse({'status': 'error', 'error_msg': 'object not found'})

        # add player move to the object
        errcode = gameobj.gameboard.make_move(player, move)
        if errcode:
            return JsonResponse({'status': 'error', 'error_msg': 'invalid player move'})

        # add cpu move to the object
        if gameobj.hardmode:
            # Easy Mode
            cpu_move = ai_simple_move(gameobj.gameboard, cpu_player)
        else:
            # Hard Mode
            cpu_move = ai_simple_move(gameobj.gameboard, cpu_player)

        if cpu_move:
            gameobj.gameboard.make_move(cpu_player, cpu_move)

        # save the object to the database
        gameobj.gameboard.save()
        gameobj.save()

        # add the cpu_move to the response and along with the status
        response_data['cpu_move'] = cpu_move or -1

    # add game data to the response
    response_data['game'] = gameobj.id
    response_data['gamestr'] = str(gameobj)
    response_data['status'] = 'success'
    response_data['gameboard'] = gameobj.gameboard.game_data
    response_data['winner'] = gameobj.gameboard.winner
    response_data['stalemate'] = gameobj.gameboard.stalemate
    response_data['moves_so_far'] = gameobj.gameboard.moves_so_far
    # add a csrf token to prevent against csrf
    response_data['csrf_token'] = str(csrf(request)['csrf_token'])

    return JsonResponse(response_data)


# Account Management Views

class UserCreate(CreateView):
    model = User
    form = UserCreationForm
    fields = ('username', 'first_name', 'last_name', 'password')
    template_name = 'exts/user_create.html'

    def get_success_url(self):
        # login the person
        self.object.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(self.request, self.object)
        # now return the success url
        return '/'

    def get_form(self, form_class=None):
        form = super(CreateView, self).get_form(form_class)
        form.fields['password'].widget = forms.PasswordInput()
        return form


class LoginView(FormView):
    success_url = '/'
    template_name = 'exts/login_form.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get('next')
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    url = '/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


# helper functions

def make_new_game_object(user, difficulty):
    # Django is kinda weird about one to one relationships
    game_board = GameBoard()
    game_board.save()
    game = Game(user=user, gameboard=game_board, hardmode=difficulty)
    game.save()
    return game


