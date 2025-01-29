from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Value, BooleanField, F, Q
from .models import Ticket, Review
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpRequest
from itertools import chain
from . import forms
from .functions import clear_messages, handle_action


@login_required
def flux(request: HttpRequest):
    """
    Vue pour afficher le flux des tickets et critiques.

    Cette vue récupère et combine les tickets et critiques de l'utilisateur,
    des utilisateurs suivis, et des critiques sur les tickets de l'utilisateur.
    Les résultats sont triés par date de création et rendus
    dans le template "website/flux.html".

    Args:
        request (HttpRequest): L'objet de requête HTTP.

    Returns:
        HttpResponse: La réponse HTTP avec le template rendu.
    """

    # Utilisateurs suivis par l'utilisateur actuel
    followed_profiles = request.user.profile.follows.all()

    # Tickets de l'utilisateur et des utilisateurs suivis
    # Ajoute un champ "is_ticket" pour distinguer les tickets des critiques
    tickets = Ticket.objects.filter(
        Q(user__profile__in=followed_profiles) | Q(user=request.user)
    ).exclude(
        Q(user__profile__blocked=request.user.profile) | Q(user__profile__in=request.user.profile.blocked.all())
    ).annotate(
        is_ticket=Value(True, output_field=BooleanField())
    ).select_related("user").order_by("-time_created")

    # Critiques de l'utilisateur et des utilisateurs suivis
    # Ajoute un champ "is_ticket" pour distinguer les critiques des tickets
    # Renomme le champ "headline" en "title"
    reviews = Review.objects.filter(
        Q(user__profile__in=followed_profiles)
        | Q(user=request.user)
        | Q(ticket__user__profile__in=followed_profiles)
    ).exclude(
        Q(user__profile__blocked=request.user.profile)
        | Q(ticket__user__profile__blocked=request.user.profile)
        | Q(user__profile__in=request.user.profile.blocked.all())
        | Q(ticket__user__profile__in=request.user.profile.blocked.all())
    ).annotate(
        is_ticket=Value(False, output_field=BooleanField()),
        title=F("headline")
    ).select_related("user", "ticket").order_by("-time_created")

    # Tickets déjà critiqués sur l'application
    reviewed_tickets = set(Review.objects.filter(
        Q(user__profile__in=followed_profiles) | Q(user=request.user)
    ).values_list("ticket_id", flat=True))

    posts = sorted(
        chain(tickets, reviews),
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
@clear_messages
def follows(request: HttpRequest):
    """
    Gère la vue pour suivre d'autres utilisateurs.

    Cette fonction affiche un formulaire permettant à l'utilisateur connecté
    de suivre d'autres utilisateurs.
    Elle traite également les soumissions de formulaire pour ajouter
    de nouveaux utilisateurs à la liste des suivis.

    Args:
        request (HttpRequest): L'objet de requête HTTP.

    Returns:
        HttpResponse: La réponse HTTP avec le rendu du template
        'website/follows.html' et le contexte mis à jour.

    Context:
        form (FollowUserForm): Le formulaire pour suivre un utilisateur.
        message (str): Un message indiquant le résultat de l'action de suivi.
        followed_users (QuerySet): La liste des utilisateurs suivis
        par l'utilisateur connecté.
        followers (QuerySet): La liste des utilisateurs qui suivent
        l'utilisateur connecté.
    """

    following = request.user.profile.follows.all()
    followers = request.user.profile.followed_by.all()
    blocked_users = request.user.profile.blocked.all()

    if request.method == "POST":
        form = forms.FollowUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]

            def action():
                if not User.objects.filter(username=username).exists():
                    raise ValueError("Cet utilisateur n'existe pas !")
                elif request.user.username == username:
                    raise ValueError(
                        "Vous ne pouvez pas vous suivre vous-même !"
                        )

                user_to_follow = User.objects.get(username=username)

                if user_to_follow.profile in following:
                    raise ValueError("Vous suivez déjà cet utilisateur !")
                else:
                    request.user.profile.follows.add(user_to_follow.profile)

            return handle_action(
                request,
                action,
                "Utilisateur suivi avec succès !",
                "Erreur lors du suivi de l'utilisateur.",
                redirect_url="follows"
            )
    else:
        form = forms.FollowUserForm()

    return render(
        request,
        "website/follows.html",
        context={
            "form": form,
            "following": following,
            "followers": followers,
            "blocked_users": blocked_users
        }
    )


@login_required
def unfollow(request: HttpRequest, user_id: str):
    """
    Permet à un utilisateur de se désabonner d'un autre utilisateur.
    Args:
        request (HttpRequest): La requête HTTP contenant les informations
        de l'utilisateur actuel.
        user_id (int): L'identifiant de l'utilisateur à désabonner.
    Returns:
        HttpResponse: Redirige vers la page des abonnements après avoir tenté
        de se désabonner.
    Raises:
        User.DoesNotExist: Si l'utilisateur à désabonner n'existe pas.
    Notes:
        - Si l'utilisateur tente de se désabonner de lui-même,
        un message d'erreur est affiché.
        - Si l'utilisateur à désabonner n'existe pas,
        un message d'erreur est affiché.
    """

    user_id = int(user_id.split("_")[-1])

    def action():
        if not User.objects.filter(id=user_id).exists():
            raise ValueError("Cet utilisateur n'existe pas !")
        elif user_id == request.user.id:
            raise ValueError(
                "Vous ne pouvez pas vous désabonner de vous-même !"
                )
        user_to_unfollow = User.objects.get(id=user_id)
        request.user.profile.follows.remove(user_to_unfollow.profile)

    return handle_action(
        request,
        action,
        "Désabonnement effectué avec succès !",
        "Erreur lors du désabonnement.",
        redirect_url="follows"
    )

@login_required
def block(request: HttpRequest, user_id: str):
    """
    Bloque un utilisateur.

    Args:
        request (HttpRequest): L'objet de la requête HTTP.
        user_id (str): L'identifiant de l'utilisateur à bloquer.

    Returns:
        HttpResponse: Redirige vers la page des abonnements après avoir bloqué
        l'utilisateur.
    """

    user_id = int(user_id.split("_")[-1])

    def action():
        if not User.objects.filter(id=user_id).exists():
            raise ValueError("Cet utilisateur n'existe pas !")
        elif user_id == request.user.id:
            raise ValueError("Vous ne pouvez pas vous bloquer vous-même !")
        user_to_block = User.objects.get(id=user_id)
        request.user.profile.blocked.add(user_to_block.profile)
        request.user.profile.follows.remove(user_to_block.profile)

    return handle_action(
        request,
        action,
        "Utilisateur bloqué avec succès !",
        "Erreur lors du blocage de l'utilisateur.",
        redirect_url="follows"
    )


@login_required
def unblock(request, user_id):
    """
    Débloque un utilisateur.

    Args:
        request (HttpRequest): L'objet de la requête HTTP.
        user_id (str): L'identifiant de l'utilisateur à débloquer.

    Returns:
        HttpResponse: Redirige vers la page des abonnements après avoir débloqué
        l'utilisateur.
    """

    user_id = int(user_id.split("_")[-1])

    def action():
        if not User.objects.filter(id=user_id).exists():
            raise ValueError("Cet utilisateur n'existe pas !")
        user_to_unblock = User.objects.get(id=user_id)
        request.user.profile.blocked.remove(user_to_unblock.profile)

    return handle_action(
        request,
        action,
        "Utilisateur débloqué avec succès !",
        "Erreur lors du déblocage de l'utilisateur.",
        redirect_url="follows"
    )


@login_required
def search_users(request: HttpRequest):
    """
    Recherche des utilisateurs dont le nom d'utilisateur
    commence par une chaîne donnée.

    Args:
        request (HttpRequest): La requête HTTP contenant
        les paramètres de recherche.

    Returns:
        JsonResponse: Une réponse JSON contenant une liste
        des noms d'utilisateur correspondant à la recherche.
    """

    if request.method == "GET":
        username = request.GET.get('search', '').strip()

        if not username:
            return JsonResponse({"users": []})

        users = (
            User.objects.filter(username__istartswith=username)
            .exclude(id=request.user.id)
            .order_by("username")[:5]
        )

        return JsonResponse(
            {"users": list(users.values("username"))})

    return JsonResponse({}, safe=False)


@login_required
@clear_messages
def create_ticket(request: HttpRequest):
    """
    Gère la création d'un ticket.

    Si la méthode de la requête est POST :
        - Valide le formulaire de création de ticket.

    Si le formulaire est valide :
        - Crée un ticket associé à l'utilisateur actuel et le sauvegarde.

    Affiche un message de succès et redirige vers la page des posts.

    Si la méthode de la requête n'est pas POST :
        - Affiche un formulaire vide pour la création de ticket.

    Args:
        request (HttpRequest): L'objet de la requête HTTP.

    Returns:
        HttpResponse: La réponse HTTP avec le formulaire de création de ticket
          ou une redirection.
    """

    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)

        def action():
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()
            else:
                raise ValueError("Erreur lors de la création du ticket.")

        return handle_action(
            request,
            action,
            "Ticket créé avec succès !",
            "Erreur lors de la création du ticket.",
            redirect_url="posts"
        )
    else:
        form = forms.TicketForm()

    return render(
        request,
        "website/create-ticket.html",
        context={
            "form": form
        }
    )


@login_required
@clear_messages
def edit_post(request, post_id, post_type):
    """
    Edite un post (ticket ou critique) existant.

    Cette vue permet à un utilisateur de modifier un post (ticket ou critique)
    qu'il a créé. Si le post n'existe pas ou si l'utilisateur n'a pas
    l'autorisation d'y accéder :
        - Un message d'erreur est affiché et l'utilisateur est redirigé
        vers la page des posts.

    Args:
        request (HttpRequest): L'objet de la requête HTTP.
        post_id (int): L'identifiant du post à modifier.
        post_type (str): Le type du post à modifier ('ticket' ou 'review').

    Returns:
        HttpResponse: La réponse HTTP avec le formulaire de modification
        du post ou une redirection.
    """

    post_model = Ticket if post_type == "ticket" else Review
    post_query = post_model.objects.filter(id=post_id, user=request.user)
    error_message = (
        f"{post_type.capitalize()} introuvable ou accès non autorisé."
    )
    success_message = f"{post_type.capitalize()} modifié avec succès !"

    if not post_query.exists():
        messages.error(request, error_message)
        return redirect("posts")

    post = post_query.first()

    if request.method == "POST":
        form = (
            forms.TicketForm(request.POST, request.FILES, instance=post)
            if post_type == "ticket"
            else forms.ReviewForm(request.POST, instance=post)
        )

        if form.is_valid():
            form.save()
            messages.success(request, success_message)
            return redirect("posts")
    else:
        form = (
            forms.TicketForm(instance=post) if post_type == "ticket"
            else forms.ReviewForm(instance=post)
        )

    template_name = (
        "website/edit-ticket.html" if post_type == "ticket"
        else "website/edit-review.html"
    )

    return render(
        request,
        template_name,
        context={
            "form": form,
            "post": post
        }
    )


@login_required
def delete_post(request, post_id, post_type):
    """
    Supprime un post (ticket ou critique) existant.

    Args:
        request (HttpRequest): L'objet de la requête HTTP.
        post_id (int): L'identifiant du post à supprimer.
        post_type (str): Le type du post à supprimer ('ticket' ou 'review').

    Returns:
        HttpResponse: Redirige vers la page des posts après la suppression
        du post.
    """

    post_model = Ticket if post_type == "ticket" else Review

    def action():
        post = post_model.objects.get(id=post_id, user=request.user)
        post.delete()

    return handle_action(
        request,
        action,
        f"{post_type.capitalize()} supprimé avec succès !",
        f"{post_type.capitalize()} introuvable ou accès non autorisé.",
        redirect_url="posts"
        )


@login_required
def posts(request):
    """
    Gère l'affichage des posts de l'utilisateur connecté.

    Cette vue récupère les tickets et les critiques créés par l'utilisateur,
    les combine, les trie par date de création décroissante et les passe au
    template pour affichage.

    Args:
        request (HttpRequest): L'objet de requête HTTP.

    Returns:
        HttpResponse: La réponse HTTP avec le template 'website/posts.html'
        et le contexte contenant les posts de l'utilisateur.

    Contexte:
        posts (list): Liste des tickets et critiques de l'utilisateur,
        triée par date de création décroissante.
    """

    tickets = (
        Ticket.objects.filter(user=request.user)
        .annotate(is_ticket=Value(True, output_field=BooleanField()))
        .select_related("user")
        .order_by("-time_created")
        )

    reviews = (
        Review.objects.filter(user=request.user)
        .annotate(
            is_ticket=Value(False, output_field=BooleanField()),
            title=F("headline")
            )
        .select_related("user", "ticket")
        .order_by("-time_created")
    )

    user_posts = sorted(
        chain(tickets, reviews),
        key=lambda x: x.time_created,
        reverse=True
    )

    return render(
        request,
        "website/posts.html",
        context={
            "posts": user_posts
        }
    )


@login_required
@clear_messages
def create_standalone_review(request):
    """
    Vue pour créer une critique indépendante avec un ticket associé.

    Cette vue gère la création d'un ticket et d'une critique associée
    lorsque la méthode de requête est POST.
    Si les formulaires de ticket et de critique sont valides,
    le ticket et la critique sont enregistrés dans la base de données.
    En cas d'erreur de validation, des messages d'erreur sont affichés
    et le ticket est supprimé si la critique n'est pas valide.

    Args:
        request (HttpRequest): L'objet de la requête HTTP.

    Returns:
        HttpResponse: Redirige vers "flux" en cas de succès ou d'erreur,
        ou rend le template "create-std-review.html" avec les formulaires
        et les messages d'erreur.
    """

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

                messages.success(request, "Critique créée avec succès !")
                return redirect("flux")
            else:
                ticket.delete()
                messages.error(
                    request, "Erreur lors de la création de la critique."
                    )
        else:
            messages.error(request, "Erreur lors de la création du ticket.")
    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()

    return render(
        request,
        "website/create-std-review.html",
        context={
            "ticket_form": ticket_form,
            "review_form": review_form
        }
    )


@login_required
@clear_messages
def create_related_review(request, ticket_id):
    """
    Vue pour créer une critique liée à un ticket existant.

    Cette vue gère la création d'une critique pour un ticket existant.

    Si la méthode de la requête est POST, elle tente de valider et
    de sauvegarder le formulaire de critique.

    En cas de succès, elle redirige vers la page "flux" avec
    un message de succès.

    En cas d'erreur de validation du formulaire, elle affiche
    un message d'erreur.

    Si la méthode de la requête n'est pas POST, elle redirige également
    vers la page "flux" avec un message d'erreur.

    Args:
        request (HttpRequest): L'objet de la requête HTTP.
        ticket_id (int): L'identifiant du ticket auquel la critique est liée.

    Returns:
        HttpResponse: Redirige vers la page "flux" en cas de succès
        ou d'erreur.
        HttpResponse: Rend la page de création de critique avec le formulaire
        en cas de méthode GET.
    """

    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)

        if review_form.is_valid():
            review: Review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            messages.success(request, "Critique créée avec succès !")
            return redirect("flux")
        else:
            messages.error(
                request, "Erreur lors de la création de la critique"
                )
    else:
        review_form = forms.ReviewForm()

    return render(
        request,
        "website/create-rel-review.html",
        context={
            "ticket": ticket,
            "review_form": review_form
        }
    )
