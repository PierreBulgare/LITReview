from django.contrib import messages
from django.core.exceptions import ValidationError
from functools import wraps
from django.http import HttpRequest
from django.shortcuts import redirect


def delete_messages(request: HttpRequest):
    """
    Supprime tous les messages stockés dans la session.
    """
    storage = messages.get_messages(request)
    for _ in storage:
        pass


def clear_messages(view_func):
    """
    Décorateur pour supprimer les messages avant d'exécuter une vue.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        delete_messages(request)
        return view_func(request, *args, **kwargs)

    return wrapper


def handle_action(
        request, action,
        success_msg, error_msg="Une erreur s'est produite.",
        redirect_url=None
        ):
    """
    Exécute une action avec gestion des messages en cas de succès ou d'échec.

    Args:
        request (HttpRequest): La requête HTTP.
        action (callable): Fonction ou lambda à exécuter.
        success_msg (str): Message de succès.
        error_msg (str, optional): Message d'erreur.
    """
    try:
        action()
        messages.success(request, success_msg)
    except ValidationError as ve:
        for error in ve.messages:
            messages.error(request, error)
    except ValueError as ve:
        messages.error(request, str(ve))
    except Exception as e:
        messages.error(request, str(e))

    if redirect_url:
        return redirect(redirect_url)
