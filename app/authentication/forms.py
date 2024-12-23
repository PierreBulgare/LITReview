from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"})
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''