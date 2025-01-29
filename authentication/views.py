from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms


def login_page(request):
    """
    Gère la page de connexion des utilisateurs.

    Si l'utilisateur est déjà authentifié, il est redirigé vers la page 'flux'.
    Sinon, un formulaire de connexion est affiché.

    Si une requête POST est reçue, les informations du formulaire sont validées
    et l'utilisateur est authentifié.

    En cas de succès, l'utilisateur est redirigé vers la page 'flux'. Sinon, un
    message d'erreur est affiché.

    Args:
        request (HttpRequest): La requête HTTP reçue du client.

    Returns:
        HttpResponse: La réponse HTTP avec le formulaire de connexion
        ou une redirection.
    """

    if request.user.is_authenticated:
        return redirect('flux')

    form = forms.LoginForm()

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            authenticate_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if authenticate_user:
                login(request, authenticate_user)
                return redirect('flux')
            else:
                messages.error(request, "Identifiants invalides !")

    return render(
        request,
        'authentication/login.html',
        context={
            'form': form
        }
    )


def logout_page(request):
    """
    Gère la déconnexion des utilisateurs.

    L'utilisateur est déconnecté et redirigé vers la page de connexion.

    Args:
        request (HttpRequest): La requête HTTP reçue du client.

    Returns:
        HttpResponse: La réponse HTTP avec une redirection
        vers la page de connexion.
    """

    messages.success(request, "Vous avez été déconnecté.")

    logout(request)

    return redirect('login')


def signup_page(request):
    """
    Gère l'inscription des nouveaux utilisateurs.

    Cette vue affiche un formulaire d'inscription et traite les données
    soumises pour créer un nouvel utilisateur.

    Si le formulaire est valide et que les mots de passe correspondent,
    un nouvel utilisateur est créé et connecté, puis redirigé
    vers la page d'accueil. Sinon, un message d'erreur approprié est affiché.

    Args:
        request (HttpRequest): L'objet de la requête HTTP.

    Returns:
        HttpResponse: La réponse HTTP avec le formulaire d'inscription
        et les messages d'erreur éventuels.
    """

    form = forms.SignUpForm()

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            # Vérifie si le nom d'utilisateur est déjà pris
            if User.objects.filter(username=username).exists():
                messages.error(
                    request, "Ce nom d'utilisateur est déjà pris !"
                    )
            elif password != confirm_password:
                messages.error(
                    request, "Les mots de passe ne correspondent pas !"
                    )
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
            'form': form
        }
    )
