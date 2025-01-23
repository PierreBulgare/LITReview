from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from . import forms

def login_page(request):
    if request.user.is_authenticated:
        return redirect('flux')
    form = forms.LoginForm()
    message = ''

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user:
                login(request, user)
                return redirect('flux')
            else:
                message = "Identifiants invalides !"

    return render(
        request,
        'authentication/login.html',
        context={
            'form': form,
            'message': message
        }
    )

def logout_page(request):
    logout(request)
    return redirect('login')

def signup_page(request):
    form = forms.SignUpForm()
    message = ''
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)

        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            confirm_password=form.cleaned_data['confirm_password']
            # Vérifie si le nom d'utilisateur est déjà pris
            if User.objects.filter(username=username).exists():
                message = "Ce nom d'utilisateur est déjà pris !"
            else:
                # Vérifie si les mots de passe correspondent
                if password != confirm_password:
                    message = "Les mots de passe ne correspondent pas !"
                else:
                    # Crée un nouvel utilisateur
                    user = User.objects.create_user(
                        username=username,
                        password=password
                    )
                    # Connecte l'utilisateur
                    login(request, user)
                    # Redirige l'utilisateur vers la page d'accueil
                    return redirect('flux')
    return render(
        request,
        'authentication/signup.html',
        context={
            'form': form,
            'message': message
        }
    )