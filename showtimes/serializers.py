from rest_framework import serializers
from movielist.models import Movie, Person
from showtimes.models import Screening, Cinema


class CinemaSerializer(serializers.HyperlinkedModelSerializer):
    movies = serializers.SlugRelatedField(many=True, queryset=Movie.objects.all(), slug_field='title')

    class Meta:
        model = Cinema
        fields = ("id", "city", "name", "movies")


class ScreeningSerializer(serializers.HyperlinkedModelSerializer):
    cinema = serializers.SlugRelatedField(queryset=Cinema.objects.all(), slug_field='name')
    movie = serializers.SlugRelatedField(queryset=Movie.objects.all(), slug_field='title')

    class Meta:
        model = Screening
        fields = ("time", "cinema", "movie")
