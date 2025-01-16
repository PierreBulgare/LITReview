from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Ticket

from . import forms

@login_required
def flux(request):
    tickets = Ticket.objects.filter(user__profile__in=request.user.profile.follows.all()).order_by('-time_created')
    return render(
        request,
        'website/flux.html',
        context={
            'tickets': tickets
            }
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
    form = forms.TicketForm()
    message = ''

    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            
            # Crée un ticket
            message = "Ticket créé avec succès !"
            return redirect('posts')
    else:
        form = forms.TicketForm()

    return render(
        request,
        'website/create-ticket.html',
        context={
            'form': form,
            'message': message
        }
    )

@login_required
def edit_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    except Ticket.DoesNotExist:
        return redirect('posts')
    
    message = ''

    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            form.save()
            message = "Post modifié avec succès !"
            return redirect('posts')
    else:
        form = forms.TicketForm(instance=ticket)

    return render(
        request,
        'website/edit-ticket.html',
        context={
            'form': form,
            'message': message,
            'ticket': ticket
        }
    )

@login_required
def delete_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id, user=request.user)
        ticket.delete()
        message = "Ticket supprimé avec succès !"
    except Ticket.DoesNotExist:
        message = "Ce ticket n'existe pas ou vous n'avez pas la permission de le supprimer."

    return redirect('posts')


@login_required
def posts(request):
    user_posts = Ticket.objects.filter(user=request.user).order_by('-time_created')

    return render(
        request,
        'website/posts.html',
        context={
            'posts': user_posts
        }
    )

@login_required
def create_standalone_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    message = ''

    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.save()

                message = "Critique créée avec succès !"
                return redirect('flux')
            else:
                ticket.delete()
                message = "Erreur lors de la création de la critique."
        else:
            message = "Erreur lors de la création du ticket."

    return render(
        request,
        'website/create-std-review.html',
        context={
            'ticket_form': ticket_form,
            'review_form': review_form,
            'message': message
        }
    )

@login_required
def create_related_review(request):
    return render(
        request,
        'website/create-rel-review.html'
    )