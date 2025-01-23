from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Value, BooleanField, F
from .models import Ticket, Review
from django.http import JsonResponse
from itertools import chain

from . import forms

@login_required
def flux(request):
    # Tickets et criqtiues de l'utilisateur connecté
    user_tickets = Ticket.objects.filter(user=request.user).annotate(
        is_ticket=Value(True, output_field=BooleanField())
    ).order_by("-time_created")

    user_reviews = Review.objects.filter(user=request.user).annotate(
        is_ticket=Value(False, output_field=BooleanField()),
        title=F("headline")  # Renommer "headline" en "title"
    ).order_by("-time_created")

    # Tickets et critiques des utilisateurs suivis
    followed_profiles = request.user.profile.follows.all()
    other_tickets = Ticket.objects.filter(user__profile__in=followed_profiles).annotate(
        is_ticket=Value(True, output_field=BooleanField())
    ).order_by("-time_created")

    other_reviews = Review.objects.filter(user__profile__in=followed_profiles).annotate(
        is_ticket=Value(False, output_field=BooleanField()),
        title=F("headline")
    ).order_by("-time_created")

    # Tickets déjà critiqués
    reviewed_tickets = Review.objects.all()


    # Combinaison des tickets et critiques triés par date de création
    posts = sorted(
        chain(user_tickets, user_reviews, other_tickets, other_reviews),
        key=lambda x: x.time_created,
        reverse=True
    )

    return render(
        request,
        "website/flux.html",
        context={
            "posts": posts,
            "reviewed_tickets": reviewed_tickets
        }
    )

@login_required
def follows(request):
    form = forms.FollowUserForm()
    message = ""
    followed_users = request.user.profile.follows.all()
    followers = request.user.profile.followed_by.all()

    if request.method == "POST":
        form = forms.FollowUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]

            try:
                user_to_follow = User.objects.get(username=username)
                print(user_to_follow)
                print(followed_users[0].user)
                if user_to_follow == request.user:
                    message = "Vous ne pouvez pas vous suivre vous-même !"
                elif user_to_follow.profile in followed_users:
                    message = "Vous suivez déjà cet utilisateur !"
                else:
                    request.user.profile.follows.add(user_to_follow.profile)
                    message = "Utilisateur suivi avec succès !"
                    followed_users = request.user.profile.follows.all()
            except User.DoesNotExist:
                message = "Cet utilisateur n'existe pas !"
            except AttributeError:
                message = "Erreur de configuration du profil utilisateur."
    return render(
        request,
        "website/follows.html",
        context={
            "form": form,
            "message": message,
            "followed_users": followed_users,
            "followers": followers
        }
    )

@login_required
def unfollow(request, user_id):
    if user_id == str(request.user.id):
        messages.error(request, "Vous ne pouvez pas vous désabonner de vous-même !")
        return redirect("follows")
    try:
        user_id = int(user_id.split("_")[-1])
        user_to_unfollow = User.objects.get(id=user_id)
        request.user.profile.follows.remove(user_to_unfollow.profile)
    except User.DoesNotExist:
        messages.error(request, "Cet utilisateur n'existe pas !")

    return redirect("follows")

@login_required
def search_users(request):
    if request.method == "GET":
        username = request.GET.get('search', '')
        users = User.objects.filter(username__startswith=username).exclude(id=request.user.id)
        return JsonResponse(
            {"users": list(users.values("username"))}, safe=False)
    return JsonResponse({}, safe=False)

@login_required
def create_ticket(request):
    form = forms.TicketForm()
    message = ""

    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            
            # Crée un ticket
            message = "Ticket créé avec succès !"
            return redirect("posts")
    else:
        form = forms.TicketForm()

    return render(
        request,
        "website/create-ticket.html",
        context={
            "form": form,
            "message": message
        }
    )

@login_required
def edit_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    except Ticket.DoesNotExist:
        return redirect("posts")
    
    message = ""

    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            form.save()
            message = "Post modifié avec succès !"
            return redirect("posts")
    else:
        form = forms.TicketForm(instance=ticket)

    return render(
        request,
        "website/edit-ticket.html",
        context={
            "form": form,
            "message": message,
            "ticket": ticket
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

    return redirect("posts")


@login_required
def posts(request):
    user_tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
    user_reviews = Review.objects.filter(user=request.user).order_by("-time_created")
    posts = list(user_tickets) + list(user_reviews)

    for ticket in user_tickets:
        ticket.is_ticket = True
    for review in user_reviews:
        review.is_ticket = False
        review.title = review.headline
        
    user_posts = sorted(posts, key=lambda x: x.time_created, reverse=True)

    return render(
        request,
        "website/posts.html",
        context={
            "posts": user_posts
        }
    )

@login_required
def create_standalone_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    message = ""

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        if ticket_form.is_valid():
            ticket: Ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            if review_form.is_valid():
                review: Review = review_form.save(commit=False)
                review.ticket = ticket
                review.user = request.user
                review.save()

                message = "Critique créée avec succès !"
                return redirect("flux")
            else:
                ticket.delete()
                message = "Erreur lors de la création de la critique."
        else:
            message = "Erreur lors de la création du ticket."

    return render(
        request,
        "website/create-std-review.html",
        context={
            "ticket_form": ticket_form,
            "review_form": review_form,
            "message": message
        }
    )

@login_required
def create_related_review(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    review_form = forms.ReviewForm()
    message = ""
    
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)

        if review_form.is_valid():
            review: Review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            message = "Critique créée avec succès !"
            return redirect("flux")
        else:
            message = "Erreur lors de la création de la critique"

    
    return render(
        request,
        "website/create-rel-review.html",
        context={
            "ticket": ticket,
            "review_form": review_form,
            "message": message
        }
    )