from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def flux(request):
    return render(
        request,
        'website/flux.html'
    )

@login_required
def follows(request):
    return render(
        request,
        'website/follows.html'
    )

@login_required
def create_ticket(request):
    return render(
        request,
        'website/create-ticket.html'
    )

@login_required
def create_standalone_review(request):
    return render(
        request,
        'website/create-std-review.html'
    )

@login_required
def create_related_review(request):
    return render(
        request,
        'website/create-rel-review.html'
    )