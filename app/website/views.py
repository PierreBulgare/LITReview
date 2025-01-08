from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from . import forms

@login_required
def flux(request):
    return render(
        request,
        'website/flux.html'
    )

@login_required
def follows(request):
    form = forms.FollowUserForm()
    message = ''
    followed_users = request.user.profile.follows.all()
    followers = request.user.profile.followed_by.all()

    if request.method == 'POST':
        form = forms.FollowUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            try:
                user_to_follow = User.objects.get(username=username)
                request.user.profile.follows.add(user_to_follow.profile)
                message = "Utilisateur suivi avec succès !"
            except User.DoesNotExist:
                message = "Cet utilisateur n'existe pas !"
            except AttributeError:
                message = "Erreur de configuration du profil utilisateur."
    return render(
        request,
        'website/follows.html',
        context={
            'form': form,
            'message': message,
            'followed_users': followed_users,
            'followers': followers
        }
    )

@login_required
def create_ticket(request):
    return render(
        request,
        'website/create-ticket.html'
    )

@login_required
def create_standalone_review(request):
    return render(
        request,
        'website/create-std-review.html'
    )

@login_required
def create_related_review(request):
    return render(
        request,
        'website/create-rel-review.html'
    )