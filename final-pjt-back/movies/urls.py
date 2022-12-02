from django.urls import path
from . import views

urlpatterns = [
    # path('data/', views.get_movie_data),
    # path('csv/', views.csv_to_DB),
    path('movies/', views.movie_list),
    path('movies/genres/', views.get_genre),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('movies/like/<int:movie_pk>/', views.movie_like),
    path('movies/like/list/<str:username>/', views.movie_like_list),
    path('movies/history/<int:movie_pk>/', views.movie_history),
    path('movies/upcoming/', views.movie_upcoming),
    path('movies/trend/', views.movie_trend),
    path('movies/poster/<int:movie_id>/', views.movie_poster),
    path('movies/likerecommend/', views.movie_recommend),
    path('movies/related/<int:movie_id>/', views.movie_related),
    path('movies/search/<str:inputData>/', views.movie_search),
    path('movies/follow/movies/<int:user_id>/', views.movie_follow_like),
    path('movies/provieder/<int:movie_id>/', views.movie_provieder),
    path('cinema/', views.cinema_list),
    path('cinema/district/<str:city>/', views.district_list),
    path('cinema/region/<str:city>/<str:district>/', views.region_list),
    path('casts/<int:movie_pk>/', views.cast_list),
]

