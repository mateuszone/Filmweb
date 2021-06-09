from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import forms, ModelForm
from basic.models import Actors, FilmReviews


# from basic.models import ExtraInfos, Profiles


# class UserForm(ModelForm):
#     class Meta:
#         models = User
#         fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
#
#
# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profiles
#         fields = ['about_me',
#                   "favourite_movie",
#                   "profile_picture"
#                   ]


class ActorForm(ModelForm):
    class Meta:
        model = Actors
        fields = ['name', 'surname', 'photo']


# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['name', 'surname', 'photo']
# UserCreationForm
class RateForm(ModelForm):
    class Meta:
        model = FilmReviews
        fields = ['user_rating', 'user_review', 'seen']
