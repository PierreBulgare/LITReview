from django import forms
from .models import Ticket, Review
from django.forms.widgets import RadioSelect
from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    """
    Un widget personnalisé pour les champs de fichier téléchargeables.
    Hérite de ClearableFileInput et utilise un modèle HTML personnalisé
    pour le rendu.

    Attributs:
    ----------
    template_name : str
        Le chemin vers le modèle HTML personnalisé utilisé
        pour le rendu du widget.
    """

    template_name = "widgets/custom_clearable_file_input.html"


class CustomRadioSelect(RadioSelect):
    """
    Une classe personnalisée pour le widget RadioSelect.

    Méthodes
    --------
    get_context(name, value, attrs)
        Retourne le contexte du widget avec une classe CSS personnalisée.
    """

    def get_context(self, name, value, attrs):
        """
        Retourne le contexte du widget avec une classe CSS personnalisée.

        Paramètres
        ----------
        name : str
            Nom du widget.
        value : str
            Valeur du widget.
        attrs : dict
            Attributs du widget.

        Retours
        -------
        dict
            Le contexte du widget avec une classe CSS personnalisée.
        """

        context = super().get_context(name, value, attrs)
        class_name = "rating"
        context['widget']['attrs']['class'] = class_name

        return context


class FollowUserForm(forms.Form):
    """
    Formulaire pour suivre un utilisateur.

    Champs:
        username (forms.CharField): Champ de saisie pour le nom d'utilisateur
        avec un maximum de 30 caractères.
            - id: "search-username"
            - placeholder: "Nom d'utilisateur"
            - autocomplete: "off"
    """

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "id": "search-username",
                "placeholder": "Nom d'utilisateur",
                "autocomplete": "off"
            }
        )
    )

    def __init__(self, *args, **kwargs):
        """
        Initialise le formulaire et supprime le label des champs.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ""


class TicketForm(forms.ModelForm):
    """
    Formulaire de création et de modification des tickets.

    Champs:
        - title: Champ de texte pour le titre du ticket,
        limité à 100 caractères.
        - description: Champ de texte pour la description (facultatif).
        - image: Champ de téléchargement d'image (facultatif).
    """

    class Meta:
        """
        Classe Meta pour le formulaire.

        Attributs:
            model (Model): Le modèle associé à ce formulaire.
            fields (list): La liste des champs à inclure dans le formulaire.
        """

        model = Ticket
        fields = ["title", "description", "image"]

    title = forms.CharField(
        max_length=100,
        label="Titre",
        widget=forms.TextInput()
    )
    description = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )
    image = forms.ImageField(
        required=False,
        widget=CustomClearableFileInput(),
    )


class ReviewForm(forms.ModelForm):
    """
    Formulaire de création de critiques.

    Ce formulaire permet de créer ou de modifier une critique.

    Champs:
    - headline : Titre de la critique, champ de texte
    avec une longueur maximale de 100 caractères.
    - rating : Note de la critique, champ de choix avec des valeurs de 0 à 5.
    - comment : Commentaire de la critique, champ de texte multiligne.

    Attributs:
        headline (CharField): Champ de texte pour le titre de la critique.
        rating (ChoiceField): Champ de choix pour la note de la revue.
        comment (CharField): Champ de texte pour le commentaire de la revue.
    """

    class Meta:
        """
        Classe Meta pour définir les métadonnées du formulaire.

        Attributs:
            model (Model): Le modèle associé au formulaire.
            fields (list): Liste des champs du modèle
            à inclure dans le formulaire.
        """

        model = Review
        fields = ["headline", "rating", "comment"]

    headline = forms.CharField(
        max_length=100,
        label="Titre",
        widget=forms.TextInput()
    )
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        label="Note",
        widget=CustomRadioSelect(
            attrs={
                "class": "rating-block"
            }
        )

    )
    comment = forms.CharField(
        label="Commentaire",
        widget=forms.Textarea()
    )
