from django.conf import settings
from django.db import models


class UserFollows(models.Model):
    """
    Le modèle UserFollows représente la relation entre les utilisateurs
    où un utilisateur en suit un autre.

    Attributs:
        user (ForeignKey): L'utilisateur qui suit un autre utilisateur.
        Référence le AUTH_USER_MODEL.
        followed_user (ForeignKey): L'utilisateur qui est suivi.
        Référence le AUTH_USER_MODEL.

    Meta:
        unique_together (tuple): Assure qu'un utilisateur ne peut pas suivre
        le même utilisateur plus d'une fois.
    """

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
        )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
        )

    class Meta:
        unique_together = ('user', 'followed_user')
