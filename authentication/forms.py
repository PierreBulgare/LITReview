from django import forms
from django.core.exceptions import ValidationError


def validate_password(password):
    """
    Valide la sécurité du mot de passe.

    Cette fonction vérifie si le mot de passe respecte les critères suivants :
    - Contient au moins 8 caractères.
    - Contient au moins un chiffre.
    - Contient au moins une lettre.

    Args:
        password (str): Le mot de passe à valider.

    Raises:
        ValidationError: Si le mot de passe ne respecte pas
        l'un des critères de sécurité.
    """

    if len(password) < 8:
        raise ValidationError(
            "Le mot de passe doit contenir au moins 8 caractères."
            )
    if not any(char.isdigit() for char in password):
        raise ValidationError(
            "Le mot de passe doit contenir au moins un chiffre."
            )
    if not any(char.isalpha() for char in password):
        raise ValidationError(
            "Le mot de passe doit contenir au moins une lettre."
            )


class LoginForm(forms.Form):
    """
    Formulaire de connexion pour les utilisateurs.

    Champs:
    - username: Champ de texte pour le nom d'utilisateur avec
    un maximum de 30 caractères.
    - password: Champ de mot de passe pour le mot de passe avec
    un maximum de 30 caractères.

    Méthodes:
    - __init__: Initialise le formulaire et supprime les label des champs.
    """

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "placeholder": "Nom d'utilisateur",
            "autocomplete": "off"
            })
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Mot de passe",
            "autocomplete": "off"
            })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ""


class SignUpForm(forms.Form):
    """
    Formulaire d'inscription pour les utilisateurs.

    Champs:
    - username: Champ de texte pour le nom d'utilisateur avec
    un maximum de 30 caractères.
    - password: Champ de mot de passe pour le mot de passe avec
    un maximum de 30 caractères.
    - confirm_password: Champ de mot de passe pour confirmer le mot de passe.

    Méthodes:
    - __init__: Initialise le formulaire et supprime les label des champs.
    """

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "placeholder": "Nom d'utilisateur",
            "autocomplete": "off"
            })
    )
    password = forms.CharField(
        max_length=30,
        validators=[validate_password],
        widget=forms.PasswordInput(attrs={
            "placeholder": "Mot de passe",
            "autocomplete": "off"
            })
    )
    confirm_password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirmer le mot de passe",
            "autocomplete": "off"
            })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ""

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password",
                           "Les mots de passe ne correspondent pas.")

        return cleaned_data
