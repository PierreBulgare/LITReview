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
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import website.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_page, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('flux/', website.views.flux, name='flux'),
    path('follows/', website.views.follows, name='follows'),
    path('search-users/', website.views.search_users, name='search_users'),
    path('posts/', website.views.posts, name='posts'),
    path('create-ticket/', website.views.create_ticket, name='create_ticket'),
    path('edit-ticket/<int:ticket_id>/', website.views.edit_ticket, name='edit_ticket'),
    path('delete-ticket/<int:ticket_id>/', website.views.delete_ticket, name='delete_ticket'),
    path('create-std-review/', website.views.create_standalone_review, name='create_standalone_review'),
    path('create-rel-review/<int:ticket_id>/', website.views.create_related_review, name='create_related_review')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)