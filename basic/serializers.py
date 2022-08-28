from .models import Films

from rest_framework import serializers


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Films

        fields = ("id", "title", "description", "premiere", "duration", "imdb_rating", "genre", "roles", "film_reviews")
