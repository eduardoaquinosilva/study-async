from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

# Create your views here.
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confimation = request.POST.get('confirm_password')

        if password != password_confimation:
            messages.add_message(request, constants.ERROR, 'Senhas não coincidem!')
            return redirect(reverse('register'))
        
        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existente!')
            return redirect(reverse('register'))
        
        try:
            User.objects.create_user(username=username, password=password)
            return redirect(reverse('login'))
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema!')
            return redirect(reverse('register'))

def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado!')
            return redirect(reverse('new_flashcard')) # not working yet
        else:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos!')
            return redirect(reverse('login'))

def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))
