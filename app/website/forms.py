from django import forms
from .models import Ticket

class FollowUserForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
    
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput()
    )
    description = forms.CharField(
        widget=forms.Textarea()
    )
    image = forms.ImageField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'title':
                field.label = 'Titre'
            else:
                field.label = ''