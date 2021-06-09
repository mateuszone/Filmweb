"""Filmweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from basic.views import Main, ActorsListView, ActorModifyView, ActorCreateView, \
    ActorDeleteView, Films, FilmCreateView, FilmModifyView, FilmDeleteView, Register, RateIt, FilmDetails, Profile, \
    RolesView, RoleModifyView, RestFilmView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('main/', Main.as_view(), name='Main'),

    path('films/', Films.as_view(), name='Films'),
    path('films/add', FilmCreateView.as_view(), name='Films_add'),
    path('films/modify/<int:pk>', FilmModifyView.as_view(), name='Films_modify'),
    path('films/delete/<int:pk>', FilmDeleteView.as_view(), name='Films_delete'),
    path('films/details/<int:id>', FilmDetails.as_view(), name='Films_details'),
    path('rate/<int:id>', RateIt.as_view(), name="Rate"),

    path('rest/<int:id>', RestFilmView.as_view(), name="Rate"),

    path('actors/', ActorsListView.as_view(), name='Actors'),
    path('actors/add/', ActorCreateView.as_view(), name='Actors_add'),
    path('actor/modify/<int:id>/', ActorModifyView.as_view(), name='Actor_modify'),
    path('actor/delete/<int:pk>/', ActorDeleteView.as_view(), name='Actor_delete'),

    path('roles/', RolesView.as_view(), name='Roles'),
    path('roles/modify/<int:pk>', RoleModifyView.as_view(), name='Role_modify'),

    # path('actor/modify/<int:id>/', ActorModifyView.as_view(), name='Actor_modify'),
    path('login/', auth_views.LoginView.as_view(), name="Login"),
    path('logout/', auth_views.LogoutView.as_view(), name="Logout"),
    path('register/', Register.as_view(), name="Register"),

    path('profile/', Profile.as_view(), name="Profile"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
