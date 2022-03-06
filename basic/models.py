from django.utils import timezone
from pyexpat import model


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# Create your models here.



class Genre(models.Model):
    # 0 = 'Undefined'
    # 1 = 'SO'
    # 2 = 'JR'
    # 3 = 'SR'
    # 4 = 'GR'
    # YEAR_IN_SCHOOL_CHOICES = [
    #     (FRESHMAN, 'Freshman'),
    #     (SOPHOMORE, 'Sophomore'),
    #     (JUNIOR, 'Junior'),
    #     (SENIOR, 'Senior'),
    #     (GRADUATE, 'Graduate'),
    # ]
    MOVIE_TYPE = {
        (0, 'Undefined'),
        (1, 'Comedy'),
        (2, 'Drama'),
        (3, 'Sci-fi'),
        (4, 'action'),
        (5, 'romantic'),
        (6, 'rom-coms'),
        (7, 'adventure'),
        (8, 'musicals'),
    }

    name = models.PositiveSmallIntegerField(default=0, choices=MOVIE_TYPE)

    def show_genre(self):
        if self.name == 0:
            return 'Undefined'
        elif self.name == 1:
            return 'Comedy'
        elif self.name == 2:
            return 'Drama'
        elif self.name == 3:
            return 'Sci-fun'
        elif self.name == 4:
            return 'Action'
        elif self.name == 5:
            return 'Romantic'
        elif self.name == 6:
            return 'Rom-coms'
        elif self.name == 7:
            return 'Adventure'
        elif self.name == 8:
            return 'Musiclas'

    def __str__(self):
        return f'{self.show_genre()}'


class Films(models.Model):
    title = models.CharField(max_length=64, blank=False, unique=True)
    description = models.TextField(default="")
    premiere = models.DateField(null=True, blank=True)
    duration = models.PositiveSmallIntegerField(default=0)
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, blank=True)
    # directed_by = models.ForeignKey("Directors", null=False, blank=False, on_delete=models.CASCADE)
    poster = models.ImageField(upload_to='posters', null=True, blank=True)
    roles = models.ManyToManyField("Actors", through='Roles', related_name='role')
    film_reviews = models.ManyToManyField(User, through='FilmReviews')
    scrapped_date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.title_with_year()

    def title_with_year(self):
        return f"{self.title} ({self.premiere})"

    def total_seen(self):
        return FilmReviews.objects.filter(seen=True, film=self).count()


class Actors(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    photo = models.ImageField(upload_to='actors', null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Roles(models.Model):
    film = models.ForeignKey(Films, on_delete=models.CASCADE, related_name='film_title')
    actor = models.ForeignKey(Actors, on_delete=models.CASCADE, related_name='actor_role')
    role_name = models.CharField(max_length=64, null=False, blank=False)

    # role_photo = models.ImageField(upload_to='roles', null=True, blank=True)
    # role_review = models.ManyToManyField(User, through='RoleReviews')

    def __str__(self):
        return f"{self.film.title} {self.actor.name} {self.actor.surname}"


class FilmReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User_FilmReviews')
    film = models.ForeignKey(Films, on_delete=models.CASCADE)
    user_rating = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
    user_review = models.TextField(null=True, blank=True)
    seen = models.BooleanField(default=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profilepic.jpg', upload_to='profiles', null=True, blank=True)
    location = models.CharField(max_length=100, default='Not your business')

    def __str__(self):
        return self.user.username

