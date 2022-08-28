import pytest
from django.contrib.auth.models import User
from django.http import request
from django.test import Client, RequestFactory

from basic.forms import RateForm
from basic.models import FilmReviews, Films, Actors, Roles
from django.core.files.uploadedfile import SimpleUploadedFile


# main działa
@pytest.mark.django_db
def test_Main():
    c = Client()
    response = c.get('/main/')
    assert "data" in response.context
    assert response.status_code == 200


# films działa
@pytest.mark.django_db
def test_Films(film):
    c = Client()
    response = c.get('/films/')
    assert response.status_code == 200
    assert len(Films.objects.all()) == 1


@pytest.mark.django_db
def test_get_FilmCreateView(genre, role, film_review):
    c = Client()
    response = c.get('/films/add')
    assert response.status_code == 200


# films/add nie działa!!
@pytest.mark.django_db
def test_post_FilmCreateView(genre, role):
    c = Client()
    film = {
        'title': 'film',
        'description': 'opis filmu',
        'premiere': '2010-10-10',
        'duration': 123,
        'imdb_rating': 8.00,
        'genre': genre.pk,
        'poster': SimpleUploadedFile(name='incepction.jpg',
                                     content=open("D:\Filmweb\my_media\posters\incepction.jpg", 'rb').read(),
                                     content_type='image/jpeg'),
        'roles': role.pk,
    }
    films_before = len(Films.objects.all())
    response = c.post('/films/add', film)
    assert films_before + 1 == Films.objects.count()
    assert response.status_code == 302


# filmmodify get
@pytest.mark.django_db
def test_get_FilmModifyView(user, genre, role, film):
    c = Client()
    c.login(username=user.username, password='Polska1992')
    response = c.get(f'/films/modify/{film.id}')
    assert 'form' in response.context
    assert response.context['form']['title'] in response.context['form']
    assert response.status_code == 200


# filmmodify post
@pytest.mark.django_db
def test_post_FilmModifyView(user, genre, role, film):
    c = Client()
    c.login(username=user.username, password='Polska1992')
    film_before = film
    movie = {
        'title': 'film',
        'description': 'opis filmu',
        'premiere': '2010-10-10',
        'duration': 123,
        'imdb_rating': 8.00,
        'genre': genre.pk,
        'poster': SimpleUploadedFile(name='incepction.jpg',
                                     content=open("D:\Filmweb\my_media\posters\incepction.jpg", 'rb').read(),
                                     content_type='image/jpeg'),
        'roles': role.pk,
    }

    response = c.post(f'/films/modify/{film.id}', movie
                      )
    assert response.status_code == 302
    assert film_before.title != Films.objects.last().title


# film delete działa
@pytest.mark.django_db
def test_get_FilmDeleteView(user, film):
    c = Client()
    c.login(username=user.username, password='Polska1992')
    response = c.get(f'/films/delete/{film.id}')
    assert response.status_code == 200


# film delete działa
@pytest.mark.django_db
def test_post_FilmDeleteView(user, film):
    c = Client()
    c.login(username=user.username, password='Polska1992')
    films_before = Films.objects.count()
    response = c.post(f'/films/delete/{film.id}')
    assert films_before > Films.objects.count()
    assert response.status_code == 302


# film details działa
@pytest.mark.django_db
def test_FilmDetails(film):
    c = Client()
    response = c.get(f'/films/details/{film.id}')
    assert response.status_code == 200
    assert 'film' in response.context
    assert 'reviews' in response.context
    assert 'roles' in response.context
    for property in response.context['form']['film'].__dict__.keys():
        assert property in ['Title',
                            'description=',
                            'premiere',
                            'duration',
                            'imdb_rating',
                            'genre']


# rate get
@pytest.mark.django_db
def test_get_Rate(user, film):
    c = Client()
    c.login(username=user.username, password='Polska1992')
    response = c.get(f'/rate/{film.id}')
    assert response.status_code == 200
    assert 'movie' in response.context
    assert 'form' in response.context


@pytest.mark.django_db
def test_post_Rate(user, film):
    c = Client()
    c.login(username=user.username, password='Polska1992')
    rates_before = FilmReviews.objects.count()
    response = c.post(f'/rate/{film.id}', {
        "user_rating": 8.00,
        "user_review": "super",
        "seen": True})
    assert 'message' in response.context
    assert 'movie' in response.context
    assert rates_before < FilmReviews.objects.count()
    assert response.status_code == 200


# actors działa
@pytest.mark.django_db
def test_ActorsListView():
    c = Client()
    response = c.get('/actors/')
    assert 'page_obj' in response.context
    assert 'roles' in response.context
    assert response.status_code == 200


# ActorCreateView/add działa
@pytest.mark.django_db
def test_get_ActorCreateView():
    c = Client()
    response = c.get('/actors/add/')
    assert 'form' in response.context
    assert response.status_code == 200


# ActorCreateView/add działa
@pytest.mark.django_db
def test_post_ActorCreateView():
    c = Client()
    actors_before = Actors.objects.count()
    response = c.post('/actors/add/', {
        "name": "name",
        "surname": "surname",
    })
    assert response.status_code == 200
    assert actors_before < Actors.objects.count()
    assert 'form' in response.context
    assert 'message' in response.context


# actor/modify_get działa
@pytest.mark.django_db
def test_get_ActorModifyView(user, actor):
    c = Client()
    c.login(username=user.username, password='Polska1992')
    response = c.get(f'/actor/modify/{actor.id}/')
    assert 'form' in response.context
    assert 'actor' in response.context
    assert response.status_code == 200


# actors/modify_post działa
@pytest.mark.django_db
def test_post_ActorModifyView(user, actor):
    c = Client()
    c.login(username=user.username, password='Polska1992')
    actor_before = actor
    response = c.post(f'/actor/modify/{actor.id}/', {
        "name": "asddssd",
        "surname": "surasddsname",
    })
    assert response.status_code == 200
    assert "message" in response.context
    assert actor_before.name != Actors.objects.last().name


# actor/delete działa
@pytest.mark.django_db
def test_get_ActorDeleteView(user, actor):
    c = Client()
    c.login(username=user.username, password='Polska1992')

    response = c.get(f'/actor/delete/{actor.id}/')
    assert response.status_code == 200


# actor/delete działa
@pytest.mark.django_db
def test_post_ActorDeleteView(user, actor):
    c = Client()
    c.login(username=user.username, password='Polska1992')
    actors_before = Actors.objects.count()
    response = c.post(f'/actor/delete/{actor.id}/')
    assert response.status_code == 302
    assert actors_before > Actors.objects.count()


# roles działa
@pytest.mark.django_db
def test_RolesView(user):
    c = Client()
    c.login(username=user.username, password='Polska1992')
    response = c.get(f'/roles/')
    assert "data" in response.context
    assert response.status_code == 200


# roles modify
@pytest.mark.django_db
def test_RoleModifyView(user, role):
    c = Client()
    c.login(username=user.username, password='Polska1992')
    role_before = role
    response = c.post(f'/roles/modify/{role.pk}', {
        'role_name': 'grazyna'
    })
    assert response.status_code == 302
    # assert 'form' in response.context nie działa
    assert role_before.role_name != Roles.objects.last().role_name


# login działa
@pytest.mark.django_db
def test_get_login(user):
    c = Client()
    response = c.get('/login/')
    assert 'form' in response.context
    assert response.status_code == 200


# login działa
@pytest.mark.django_db
def test_post_login(user):
    login_data = {
        'username': user.username,
        'password': "Polska1992"
    }
    c = Client()
    response = c.post('/login/', login_data)
    assert response.status_code == 302


# logout działa
@pytest.mark.django_db
def test_get_logout(user):
    c = Client()
    c.login(username=user.username, password="Polska1992")
    response = c.get('/logout/')
    assert response.status_code == 302


# logout działa
@pytest.mark.django_db
def test_post_logout(user):
    c = Client()
    c.login(username=user.username, password="Polska1992")
    response = c.get('/logout/')
    assert response.status_code == 302


# logout działa
@pytest.mark.django_db
def test_post_logout(user):
    c = Client()
    c.login(username=user.username, password="Polska1992")
    response = c.post('/logout/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_register():
    c = Client()
    response = c.get('/register/')
    assert "form" in response.context
    assert response.status_code == 200


# register działa
@pytest.mark.django_db
def test_post_register():
    register_data = {
        'username': 'dupa',
        'password1': "Polska1992",
        'password2': "Polska1992",
    }
    c = Client()
    users_before = User.objects.count()
    response = c.post('/register/', register_data)
    User.objects.get(username='dupa')
    assert response.status_code == 200
    assert "message" in response.context
    assert users_before < User.objects.count()


# profile działa
@pytest.mark.django_db
def test_profile(user):
    c = Client()
    c.login(username=user.username, password="Polska1992")
    response = c.get('/profile/')
    assert "user_info" in response.context
    assert "reviews" in response.context
    assert "seen_list" in response.context
    assert "films" in response.context
    assert response.status_code == 200
