from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Max, Min, Avg

# Create your views here.
from .models import Movie


def show_all_movies(request):
    movies = Movie.objects.order_by('name')
    agg = movies.aggregate(Avg('budget'), Max('rating'), Min('rating'), Count('id'))
    return render(request, 'movie_app/all_movies.html', {
        'movies': movies,
        'agg': agg
    })


def show_one_movie(request, slug_movie: str):
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, 'movie_app/one_movie.html', {
        'movie': movie
    })
