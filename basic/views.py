import asyncio
import os
import re
from datetime import datetime
from pprint import pprint

import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.views import View
from django.views.generic import UpdateView, DeleteView, CreateView
# DRF imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from basic.forms import ActorForm, RateForm, AboutForm, SearchForm
from basic.models import Actors, Films as Movie, FilmReviews, Roles
from .scraping import get_today_filmweb_urls, get_filmweb_content
from .serializers import FilmSerializer
from .utils import create_pagination, get_response_data, change_response_dict_to_queryset, shorten_url


class Main(View):
    def get(self, request):
        return render(request, 'main.html')


class Premieres(View):
    def get(self, request):
        last_scrapped_date = Movie.objects.last().scrapped_date
        days_diff = datetime.date(datetime.now()) - last_scrapped_date
        if days_diff.days > 7:
            urls = get_today_filmweb_urls()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            data_ctx = loop.run_until_complete(get_filmweb_content(urls))
            loop.close()
            for title, info_list in data_ctx.items():
                try:
                    obj, created = Movie.objects.get_or_create(
                        title=title,
                        description=info_list[1],
                        poster=info_list[0],
                        duration=info_list[2],
                        premiere=info_list[3]
                    )
                except IntegrityError:
                    pass
        movies = Movie.objects.all()
        page_obj = create_pagination(request, movies, 6, 1)
        ctx = {
            'page_obj': page_obj,
        }
        return render(request, 'premieres.html', ctx)


class MovieSearch(View):
    def get(self, request):
        form = SearchForm()
        ctx = {
            'form': form,
        }
        return render(request, 'search.html', ctx)

    def post(self, request):
        search = request.POST.get('search')
        if search is not None and search != '':
            response_data = get_response_data(search, multi=False)
            if response_data and response_data['Response'] == 'True':
                movie = change_response_dict_to_queryset(Movie, response_data)
                ctx = {
                    'film': movie,
                }
                return render(request, 'api_detail.html', ctx)
            return render(request, 'search.html', {'error': 'No results found'})
        return redirect('Search')


class AddMovieFromIMDB(View):
    def get(self, request, id):
        response_data = get_response_data('61bd6151', multi=False, imdb_id=id)
        if response_data:
            if not Movie.objects.filter(title=response_data['Title']).exists():
                if response_data['Released'] != 'N/A':
                    premiere = datetime.strptime(response_data['Released'], '%d %b %Y').strftime("%Y-%m-%d")
                else:
                    premiere = '1800-01-01'
                if response_data['Runtime'] != 'N/A':
                    runtime = int(re.findall('([^\s]+)', response_data['Runtime'])[0])
                else:
                    runtime = 0
                if response_data['imdbRating'] != 'N/A':
                    rating = float(response_data['imdbRating'])
                else:
                    rating = 0
                new_poster_url = shorten_url(response_data['Poster'])
                new_movie = Movie.objects.create(
                    title=response_data['Title'],
                    description=response_data['Plot'],
                    poster=new_poster_url,
                    duration=runtime,
                    premiere=premiere,
                    imdb_rating=rating,
                )
                new_movie.save()
                return redirect('Films_details', Movie.objects.get(pk=new_movie.pk).pk)
            return redirect('Films_details', Movie.objects.get(title=response_data['Title']).pk)
        return render(request, 'add_movie.html', {"error": "Couldn't find movie"})


class ActorsListView(View):
    def get(self, request):
        roles = Roles.objects.all
        actors = Actors.objects.order_by('surname')
        paginator = Paginator(actors, 10)
        page = request.GET.get('page', 1)

        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
        ctx = {"page_obj": page_obj,
               "roles": roles}
        return render(request, 'actors.html', ctx)


class ActorModifyView(LoginRequiredMixin, View):

    def get(self, request, id):
        actors = Actors.objects.all()
        actor = get_object_or_404(actors, pk=id)
        form = ActorForm(instance=actor)
        ctx = {'form': form, 'actor': actor}
        return render(request, 'actor_edit.html', ctx)

    def post(self, request, id):
        actor = Actors.objects.get(pk=id)
        form = ActorForm(request.POST, request.FILES)
        if not form.is_valid():
            message = "Wrong typo"
            return render(request, 'actor_edit.html', {'message': message})
        actor.name = form.cleaned_data['name']
        actor.surname = form.cleaned_data['surname']
        actor.photo = form.cleaned_data['photo']
        actor.save()
        return redirect('Actors')


# ten moze zostac generic
class ActorDeleteView(LoginRequiredMixin, DeleteView):
    model = Actors
    success_url = '/actors/'


class ActorCreateView(View):
    def get(self, request):
        form = ActorForm()
        return render(request, 'basic/actors_form.html', {"form": form})

    def post(self, request):
        form = ActorForm(request.POST, request.FILES)
        if form.is_valid():
            Actors.objects.create(name=form.cleaned_data['name'],
                                  surname=form.cleaned_data['surname'],
                                  photo=form.cleaned_data['photo'])
            return redirect('Actors')


class Films(View):
    def get(self, request):
        movies = Movie.objects.order_by('imdb_rating')
        paginator = Paginator(movies, 10)
        page = request.GET.get('page', 1)
        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        return render(request, 'films.html', {"page_obj": page_obj})


class FilmCreateView(CreateView):
    model = Movie
    fields = ['title', 'description', 'premiere', 'duration', 'imdb_rating', 'genre', 'poster', 'roles']
    success_url = '/films/'


class FilmModifyView(LoginRequiredMixin, UpdateView):
    model = Movie
    fields = ['title', 'description', 'premiere', 'duration', 'imdb_rating', 'genre', 'poster', 'roles']
    template_name_suffix = '_update_form'
    success_url = '/films/'


class FilmDeleteView(LoginRequiredMixin, DeleteView):
    model = Movie
    success_url = '/films/'


class Register(View):

    def get(self, request):
        form = UserCreationForm()
        ctx = {
            "form": form,
        }
        return render(request, 'register.html', ctx)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            ctx = {
                "form": form,
            }
            return render(request, 'register.html', ctx)
        user = form.save()
        user.refresh_from_db()
        user.save()
        request.session['message_from_registration'] = "User successfully created, please log in!"
        return redirect('Login')


class RateIt(LoginRequiredMixin, View):
    def get(self, request, id):
        movie = Movie.objects.get(pk=id)
        form = RateForm()

        ctx = {'movie': movie,
               'form': form,
               }
        return render(request, 'rate_movie.html', ctx)

    def post(self, request, id):
        movie = Movie.objects.get(pk=id)
        form = RateForm(request.POST)
        if not form.is_valid():
            message = 'Please fill all fields'
            return render(request, 'rate_movie.html', {'message': message,
                                                       'form': form,
                                                       'movie': movie,
                                                       })
        FilmReviews.objects.create(user=request.user,
                                   film=movie,
                                   user_rating=form.cleaned_data['user_rating'],
                                   user_review=form.cleaned_data['user_review'],
                                   seen=form.cleaned_data['seen']
                                   )
        message = "Thank you for your opinion"
        return render(request, 'rate_movie.html', {'message': message, 'movie': movie})


class FilmDetails(LoginRequiredMixin, View):
    def get(self, request, id):
        film = Movie.objects.get(id=id)
        rate_form = RateForm()
        reviews = film.reviews.all()
        roles = film.roles.all()
        ctx = {'film': film,
               'reviews': reviews,
               "roles": roles,
               "rate_form": rate_form}
        return render(request, 'film_details.html', ctx)

    def post(self, request, id):
        film = Movie.objects.get(id=id)
        roles = film.roles.all()
        reviews = film.reviews.all()
        rate_form = RateForm(request.POST)
        ctx = {'film': film,
               'reviews': reviews,
               "roles": roles,
               "rate_form": rate_form}
        if not rate_form.is_valid():
            return render(request, 'film_details.html', ctx)
        new_review = FilmReviews.objects.create(user=request.user,
                                                film=film,
                                                user_rating=rate_form.cleaned_data['user_rating'],
                                                user_review=rate_form.cleaned_data['user_review'],
                                                seen=rate_form.cleaned_data['seen']
                                                )
        new_review.save()
        return render(request, 'film_details.html', ctx)


class Profile(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        form = AboutForm(instance=user.profile)
        user_reviews = FilmReviews.objects.filter(user=user).distinct()
        ctx = {"username": request.user.username,
               "user_reviews": user_reviews,
               "form": form,
               }
        return render(request, 'profile.html', ctx)

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        form = AboutForm(request.POST)
        user_reviews = FilmReviews.objects.filter(user=user).distinct()
        if not form.is_valid():
            ctx = {"username": request.user.username,
                   "user_reviews": user_reviews,
                   "form": form,
                   }
            return render(request, 'profile.html', ctx)
        about = form.cleaned_data['about']
        user.profile.about = about
        user.profile.save()
        ctx = {"username": request.user.username,
               "user_reviews": user_reviews,
               "form": form,
               }
        return render(request, 'profile.html', ctx)


class RolesView(LoginRequiredMixin, View):
    def get(self, request):
        data = Roles.objects.all()
        ctx = {"data": data}
        return render(request, 'roles.html', ctx)


class RoleModifyView(LoginRequiredMixin, UpdateView):
    model = Roles
    fields = ['role_name']
    template_name_suffix = '_update_form'
    success_url = '/roles/'


class RestFilmView(APIView):
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        film = self.get_object(id)
        serializer = FilmSerializer(film, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, id, format=None):
        film = self.get_object(id)
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id, format=None):
        film = self.get_object(id)
        serializer = FilmSerializer(film, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
