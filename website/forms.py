from django import forms
from .models import Ticket, Review

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
        widget=forms.Textarea(),
        required=False
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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'description', 'rating']

    headline = forms.CharField(
        max_length=100,
        widget=forms.TextInput()
    )
    rating = forms.IntegerField(
        min_value=0,
        max_value=5,
        widget=forms.NumberInput()
    )
    description = forms.CharField(      
        widget=forms.Textarea()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'title':
                field.label = 'Titre'
            elif field_name == 'rating':
                field.label = 'Note'
            elif field_name == 'description':
                field.label = 'Commentaire'
            else:
                field.label = ''