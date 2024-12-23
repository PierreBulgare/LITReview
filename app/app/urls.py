"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import authentication.views
import website.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('flux/', website.views.flux, name='flux'),
    path('follows/', website.views.follows, name='follows'),
    path('create-ticket/', website.views.create_ticket, name='create_ticket'),
    path('create-std-review/', website.views.create_standalone_review, name='create_standalone_review'),
    path('create-rel-review/', website.views.create_related_review, name='create_related_review')
]
