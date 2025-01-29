import os
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify


def validate_image_extension(value):
    """
    Valide l'extension d'un fichier image.

    Cette fonction vérifie si l'extension du fichier fourni
    est parmi les extensions acceptées (JPG, JPEG, PNG, GIF).
    Si l'extension n'est pas acceptée, une ValidationError est levée.

    Args:
        value (File): Le fichier dont l'extension doit être validée.

    Raise:
        ValidationError: Si l'extension du fichier n'est pas parmi
        les extensions acceptées.
    """

    ext = value.name.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png', 'gif']:
        raise ValidationError(
            "Seuls les fichiers JPG, JPEG, PNG et GIF sont acceptés."
            )


def ticket_image_upload_path(instance, filename: str):
    """
    Génère le chemin de téléchargement pour une image de ticket.

    Le nom du fichier est basé sur le titre du ticket transformé en slug,
    suivi d'un UUID.
    Le chemin final est construit en utilisant
    l'ID de l'utilisateur associé à l'instance.

    Args:
        instance: L'instance du modèle Ticket contenant l'image.
        filename (str): Le nom original du fichier de l'image.
    Returns:
        str: Le chemin de téléchargement formaté pour l'image du ticket.
    """

    # Récupérer l'extension du fichier
    ext = filename.split('.')[-1].lower()

    # Générer un slug du titre du ticket
    basename = slugify(instance.title)  # Utilisation du titre du ticket

    # Récupérer l'ID du ticket si disponible, sinon utiliser un UUID temporaire
    image_id = uuid.uuid4().hex[:8]

    # Construire le chemin final
    return os.path.join(
        'tickets', f'user_{instance.user.id}', f"{basename}-{image_id}.{ext}"
        )


class Profile(models.Model):
    """
    Modèle représentant un profil utilisateur dans l'application.

    Attributs:
    ----------
    user : OneToOneField
        Une relation un-à-un avec le modèle User.
        Supprime le profil si l'utilisateur est supprimé.
    follows : ManyToManyField
        Une relation plusieurs-à-plusieurs avec d'autres profils.
        Permet de suivre des utilisateurs.
    blocked : ManyToManyField
        Une relation plusieurs-à-plusieurs avec d'autres profils.
        Permet de bloquer des utilisateurs.

    Méthodes:
    ---------
    __str__():
        Retourne le nom d'utilisateur associé au profil.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
        )
    follows = models.ManyToManyField(
        'self', symmetrical=False, related_name='followed_by', blank=True
        )
    blocked = models.ManyToManyField(
        'self', symmetrical=False, related_name='blocked_by', blank=True
        )

    def __str__(self):
        return self.user.username


class Ticket(models.Model):
    """
    Modèle représentant un ticket.

    Attributs:
        title (CharField): Titre du ticket (128 caractères max, unique).
        description (TextField): Description du ticket.
        user (ForeignKey): Utilisateur associé au ticket,
        référence le modèle utilisateur défini dans les paramètres.
        image (ImageField): Image associée au ticket, peut être vide ou nulle.
        time_created (DateTimeField): Date et heure de création du ticket,
        définie automatiquement à la création.

    Méthodes:
        __str__: Retourne le titre du ticket.
    """

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
        )
    image = models.ImageField(
        upload_to=ticket_image_upload_path,
        null=True, blank=True,
        validators=[validate_image_extension]
        )
    time_created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validation pour éviter un titre dupliqué pour un même utilisateur"""
        if not hasattr(self, "user") or self.user is None:
            return

        if (
            Ticket.objects.filter(user=self.user, title=self.title)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                f"Vous avez déjà créé un ticket pour ({self.title})."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Modèle représentant une critique d'un ticket.

    Attributs:
        ticket (ForeignKey): Référence au ticket associé à cette critique.
        rating (PositiveSmallIntegerField): Note de la critique (0 à 5).
        user (ForeignKey): Utilisateur qui a créé la critique.
        headline (CharField): Titre de la critique (128 caractères max).
        comment (TextField): Commentaire de la critique, peut être vide.
        time_created (DateTimeField): Date et heure de création de la critique,
        définie automatiquement à la création.
    """

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
        )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
        )
    headline = models.CharField(max_length=128)
    comment = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Crée un profil utilisateur lorsque l'instance utilisateur est créée.
    Args:
        sender (Model): Le modèle qui envoie le signal.
        instance (User): L'instance de l'utilisateur qui a été créée.
        created (bool): Indique si l'instance a été créée (True)
        ou mise à jour (False).
    """

    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Enregistre le profil associé à une instance donnée.

    Cette fonction est généralement utilisée comme un gestionnaire de signal
    pour sauvegarder automatiquement le profil
    lorsqu'une instance est sauvegardée.

    Args:
        sender (type): La classe de l'instance qui envoie le signal.
        instance (object): L'instance de l'objet qui est sauvegardée.
    """

    if hasattr(instance, 'profile'):
        instance.profile.save()
