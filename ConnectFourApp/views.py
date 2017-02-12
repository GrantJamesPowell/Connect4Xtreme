# Django View Functions
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, RedirectView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout

# Models
from django.contrib.auth.models import User
from .models import Game, GameBoard

# forms
from django import forms

# Game Views

class HomePage(ListView):
    model = Game


class GameView(TemplateView):
    pass


# Account Management Views

class UserCreate(CreateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'password')
    template_name = 'exts/user_create.html'

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
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)