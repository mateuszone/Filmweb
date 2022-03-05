from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from bs4 import BeautifulSoup
# Create your views here.
from django.views import View
import requests
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, FormView, UpdateView, DeleteView, CreateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from basic.forms import ActorForm, RateForm
from basic.models import Actors, Films as Movie, FilmReviews, Roles

from collections import Counter
from django.http import Http404
from django.utils import timezone

# DRF imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FilmSerializer


class Main(View):
    def get(self, request):
        movies = Movie.objects.filter(scrapped_date=timezone.now())
        if len(movies) == 0:
            number_of_movies = 10
            response = requests.get("https://www.filmweb.pl/ranking/wantToSee/next30daysPoland")
            premiery = response.text

            soup = BeautifulSoup(premiery, "html.parser")
            premiery = soup.select('.rankingType__header')
            zdjecia = soup.select("a img ")

            premiery = [film.getText()[:film.getText().index('2')] for film in premiery]
            zdjecia = [zdjecie.get('data-src') for zdjecie in zdjecia[:len(premiery[:number_of_movies]) - 1]]

            linki = soup.select('div .rankingType__title a')
            descriptions = []
            for link in linki[:11]:
                response = requests.get(f"https://www.filmweb.pl{link.get('href')}")
                response = response.text

                soup = BeautifulSoup(response, "html.parser")
                description = soup.select('div .filmPosterSection__plot')
                for x in description:
                    try:
                        descriptions.append(x.text.rsplit(".", 1)[0])
                    except:
                        pass
            data_ctx = {premiery[x]: [zdjecia[x], descriptions[x]] for x in range(0, len(premiery[:number_of_movies]) - 1)}
            added = 0
            for title, info_list in data_ctx.items():
                obj, created = Movie.objects.get_or_create(
                    title=title,
                    description=info_list[1],
                    poster=info_list[0],
                )
                if created:
                    added += 1
            print(f"Dodano {added}")
            ctx = {
                'data': data_ctx
            }
        else:
            ctx = {
                'data': movies,
                'queryset': True
            }
        return render(request, 'main.html', ctx)


class ActorsListView(View):
    def get(self, request):
        roles = Roles.objects.all
        actors = Actors.objects.order_by('surname')
        paginator = Paginator(actors, 3)
        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)

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
        if form.is_valid():
            actor.name = form.cleaned_data['name']
            actor.surname = form.cleaned_data['surname']
            actor.photo = form.cleaned_data['photo']
            actor.save()
            message = "User successfully updated"
            return render(request, 'actor_edit.html', {'form': form, 'message': message})
        else:
            message = "Wrong typo"
            return render(request, 'actor_edit.html', {'message': message})


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
            message = "User successfully created"
            return render(request, 'basic/actors_form.html', {'form': form, 'message': message})


class Films(View):
    def get(self, request):
        film_list = Movie.objects.order_by('imdb_rating')
        paginator = Paginator(film_list, 5)
        page = request.GET.get('page', 1)
        rate = FilmReviews.objects.all()
        dict = {}
        for x in rate:
            id = x.film_id
            rating = float(x.user_rating)
            try:
                dict[id].append(rating)
            except KeyError:
                dict[id] = [rating]
        rate_dict = {k: sum(v) / len(v) for (k, v) in dict.items()}
        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        return render(request, 'films.html', {"page_obj": page_obj,
                                              "rate": rate,
                                              'rate_dict': rate_dict
                                              })

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
        if form.is_valid():
            form.save()
            message = 'User succesfully created'
            ctx = {
                "message": message,
            }
            return render(request, 'register.html', ctx)
        else:
            message = 'Please fill the form again'
            ctx = {
                "form": form,
                "message": message,
            }
            return render(request, 'register.html', ctx)


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
        if form.is_valid():
            FilmReviews.objects.create(user=request.user,
                                       film=movie,
                                       user_rating=form.cleaned_data['user_rating'],
                                       user_review=form.cleaned_data['user_review'],
                                       seen=form.cleaned_data['seen']
                                       )
            message = "Thank you for your opinion"
            return render(request, 'rate_movie.html', {'message': message, 'movie': movie})
        else:
            message = 'Please fill all fields'
            return render(request, 'rate_movie.html', {'message': message,
                                                       'form': form,
                                                       'movie': movie,
                                                       })

class FilmDetails(View):
    def get(self, request, id):
        film = Movie.objects.get(id=id)
        roles = Roles.objects.all()
        reviews = FilmReviews.objects.all()
        ctx = {'film': film,
               'reviews': reviews,
               "roles": roles}
        return render(request, 'film_details.html', ctx)


class Profile(LoginRequiredMixin, View):
    def get(self, request):
        films = Movie.objects.all()
        User_info = request.user.username
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        reviews = FilmReviews.objects.filter(user=user).distinct()
        seen_dict = {}
        all_user_movies_reviews = [movie.film.title for movie in reviews.all() if movie.seen == True]
        user_movie_list = [*Counter(all_user_movies_reviews)]
        for movie in reviews.all():
            if movie.seen:
                seen_dict[movie.film.title] = movie.user_rating
        ctx = {"user_info": User_info,
               "reviews": reviews,
               "seen_list": user_movie_list,
               "films": films
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
