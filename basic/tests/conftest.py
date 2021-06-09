import pytest
from basic.models import User, Genre, Films, Actors, Roles, FilmReviews


@pytest.fixture
def user():
    user = User.objects.create_user(username='testowy', email='email@gmail.com', password='Polska1992')
    return user

@pytest.fixture
def genre():
    genre = Genre.objects.create(name=1)
    return genre


@pytest.fixture
def actor():
    actor = Actors.objects.create(id="1",name='Mateusz', surname='Czaja')
    return actor


@pytest.fixture
def film(genre):
    film = Films.objects.create(
        title='shawnshan',
        description='super film',
        premiere='2010-10-10',
        duration=20,
        imdb_rating=9.00,
        genre=genre,
        # poster='zdjecie'
    )
    return film


@pytest.fixture
def role(film, actor):
    role = Roles.objects.create(
        pk=1,
        film=film,
        actor=actor,
        role_name='Killer'
    )
    return role


@pytest.fixture
def film_review(user,film):
    film = FilmReviews.objects.create(
        user=user,
        film=film,
        user_rating='9.00',
        user_review='swietny film',
        seen='True'
    )
    return film