from django.contrib import admin
from .models import *


# Register your models here.

# @admin.register(Films)
# class FilmAdmin(admin.ModelAdmin):
#     fields = ['title', 'description', 'premiere', 'imdb_rating', 'genre']
#     list_display = ['title', 'description', 'premiere', 'imdb_rating', 'genre']
#     list_filter = ("premiere", "imdb_rating", 'genre')
#     search_fields = ("title", "description", "premiere", 'genre')


admin.site.register(Genre)
admin.site.register(Films)
admin.site.register(Actors)
admin.site.register(Roles)
admin.site.register(Profile)
# admin.site.register(RoleReviews)
admin.site.register(FilmReviews)
# admin.site.register(Profiles)
# admin.site.register(Directors)
# admin.site.register(Messages)
