from django.db import models
from django.conf import settings


# N대 M을 위한 번호별 장르 이름을 담는 테이블
# TMDB는 장르가 숫자로 표현되어 이름으로 변형이 필요
class Genre(models.Model):
    name = models.CharField(max_length=50)


# 영화에 대한 세부 정보 테이블
class Movie(models.Model):
    title = models.CharField(max_length=100)
    movie_id = models.CharField(max_length=10)
    poster_path = models.CharField(max_length=200, null=True)
    release_date = models.DateField()
    overview = models.TextField()
    video_path = models.CharField(max_length=100, null=True)
    genres = models.ManyToManyField(Genre)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies")
    vote_average = models.FloatField()
    recommend_movie_id = models.CharField(max_length=100)
    

# 스트리밍(넷플릭스, 왓챠 등) 정보를 담는 테이블
class Provider(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    provider_link = models.CharField(max_length=200)
    provider_logo_path = models.CharField(max_length=200)


# 영화별 배우, 감독 정보 테이블
class Cast(models.Model):
    name = models.CharField(max_length=50)
    known_for_department = models.CharField(max_length=20)
    movie_id = models.CharField(max_length=10)
    credit_id = models.CharField(max_length=50)


# 영화별 포스터 URL을 출력하기 위한 테이블
class Poster(models.Model):
    movie_id = models.CharField(max_length=100)
    file_path = models.CharField(max_length=200)


# 유저의 클릭 활동 기록
class History(models.Model):
    user_id = models.IntegerField()
    movie_id = models.CharField(max_length=10)
    genres = models.IntegerField()
    score = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)


# 영화관 주소 정보 데이터
class Cinema(models.Model):
    name = models.CharField(max_length=50)
    metropolitan_city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    latitude = models.FloatField()
    altitude = models.FloatField()