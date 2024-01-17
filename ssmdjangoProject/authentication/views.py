import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserCreationForm, LoginForm

logger = logging.getLogger(__name__)


def index(request):
    logger.info('Index-Seite wurde aufgerufen.')
    return render(request, 'index.html')


@login_required
def privatepage(request):
    logger.info(f'Private Seite aufgerufen von Benutzer: {request.user.username}')
    return render(request, 'privatepage.html')


def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f'Neuer Benutzer registriert: {form.cleaned_data["username"]}')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                logger.info(f'Benutzer {username} erfolgreich angemeldet.')
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    logger.info(f'Benutzer {request.user.username} hat sich abgemeldet.')
    return redirect('login')
