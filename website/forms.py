from django import forms
from .models import Ticket, Review
from django.forms.widgets import RadioSelect
from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    template_name = "widgets/custom_clearable_file_input.html"


class CustomRadioSelect(RadioSelect):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        class_name = "rating"
        context['widget']['attrs']['class'] = class_name
        return context


class FollowUserForm(forms.Form):
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
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ""


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

    title = forms.CharField(
        max_length=100,
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "title":
                field.label = "Titre"
            elif field_name == "description":
                field.label = "Description"
            elif field_name == "image":
                field.label = "Image"
            else:
                field.label = ""


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "comment"]

    headline = forms.CharField(
        max_length=100,
        widget=forms.TextInput()
    )
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=CustomRadioSelect(
            attrs={
                "class": "rating-block"
            }
        )

    )
    comment = forms.CharField(
        widget=forms.Textarea()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ["title", "headline"]:
                field.label = "Titre"
            elif field_name == "rating":
                field.label = "Note"
            elif field_name == "comment":
                field.label = "Commentaire"
            else:
                field.label = ""
