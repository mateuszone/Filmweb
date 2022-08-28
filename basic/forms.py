from django.forms import ModelForm
from django import forms
from basic.models import Actors, FilmReviews, Profile


class ActorForm(ModelForm):
    class Meta:
        model = Actors
        fields = ['name', 'surname', 'photo']


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label='')


class RateForm(ModelForm):
    class Meta:
        model = FilmReviews
        fields = ['user_rating', 'user_review', 'seen']


class AboutForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['about']
        labels = {
            "about": ""
        }
