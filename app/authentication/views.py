from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from . import forms

def login_page(request):
    form = forms.LoginForm()
    message = ''

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user:
                login(request, user)
                return redirect('flux')
            else:
                message = "Identifiants invalides !"

    return render(
        request,
        'authentication/login.html',
        context={
            'form': form,
            'message': message
        }
    )

def signup_page(request):
    return render(
        request,
        'authentication/signup.html'
    )