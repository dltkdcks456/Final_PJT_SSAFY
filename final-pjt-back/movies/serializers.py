from rest_framework import serializers
from .models import Movie, Genre, Cast, Poster, Provider, Cinema

class CastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cast
        fields = ('name', 'known_for_department', 'movie_id', 'credit_id')


class MovieListSerializer(serializers.ModelSerializer):


    class Meta:
        model = Movie
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

class GenreListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

class PosterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poster
        fields = '__all__'

class ProviderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Provider
        fields = '__all__'

class CinemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cinema
        fields = '__all__'