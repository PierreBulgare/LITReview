from django import forms


class LoginForm(forms.Form):
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
