from django.http import HttpResponse, JsonResponse
import json
import random
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import MovieListSerializer, MovieSerializer, CastSerializer, PosterSerializer ,GenreListSerializer, ProviderSerializer, CinemaSerializer
from .models import Movie, Genre, Cast, Poster, History, Provider, Cinema
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from django.utils import timezone
import pandas


# def csv_to_DB(request):
'''
example.csv이라는 영화관 공공데이터를 통해 csv를 DB에 저장하는 함수
[문제사항]: 위도와 경도는 문자로 저장되기 때문에 추후에 숫자로 바꿔야한다.
'''
#     data = pandas.read_csv("./movies/example.csv")
#     filter_data = data.filter(items=['POI_NM', 'CTPRVN_NM','SIGNGU_NM', 'LEGALDONG_NM', 'LC_LO', 'LC_LA'])
#     total_cnt = len(filter_data)
#     for i in range(total_cnt):
#         Cinema.objects.create(
#             name = filter_data.loc[i][0],
#             metropolitan_city = filter_data.loc[i][1],
#             district = filter_data.loc[i][2],
#             region = filter_data.loc[i][3],
#             latitude = filter_data.loc[i][4],
#             altitude = filter_data.loc[i][5]
#             )
    
@api_view(['GET'])
def cinema_list(request):
    '''
    주어진 3가지의 주소 데이터(광역시, 구, 동)를 통해 해당 영화관 찾아서 반환하는 함수
    [아이디어]: 카카오 맵을 표현할 때 지역 단위로 구분하고 싶었다.
    '''
    metropolitan_city = request.GET.get('metropolitan_city')
    district = request.GET.get('district')
    region = request.GET.get('region')
    cinema = Cinema.objects.filter(metropolitan_city=metropolitan_city).filter(district=district).filter(region=region)
    if len(cinema) == 1:
        serializer = CinemaSerializer(cinema[0])
        return Response(serializer.data)
    elif len(cinema) >= 2:
        serializer = CinemaSerializer(cinema, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def district_list(request, city):
    '''
    city를 선택하고 나서 데이터를 받은 후에 district의 옵션을 결정해주기 위한 함수
    예를 들어, 강원도가 선택되어지면 그에 따른 구들이 옵션에 나타나도록 할 예정
    '''
    cinemas = Cinema.objects.filter(metropolitan_city=city)
    selectcity = cinemas.order_by('district')
    results = selectcity.values_list('district', flat=True).distinct()
    return Response(results)


@api_view(['GET'])
def region_list(request, city, district):
    '''
    광역시와 구의 정보를 바탕으로 도를 파악하는 함수
    [문제상황] 광역시의 필터를 걸어주지 않으니 다른 광역시와 같은 구가 겹쳐서 나오는 경우가 생겼었다
    '''
    cinemas = Cinema.objects.filter(metropolitan_city=city).filter(district=district)
    selectcity = cinemas.order_by('region')
    results = selectcity.values_list('region', flat=True).distinct()
    return Response(results)


@api_view(['GET'])
def movie_provieder(request, movie_id):
    '''
    스트리밍(넷플릭스, 왓챠 등)에 대한 정보를 불러오는 함수
    '''
    providers = get_list_or_404(Provider, movie_id = movie_id)
    serializer = ProviderSerializer(providers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_upcoming(request):
    '''
    최근 30일의 영화를 뽑아와서 현재 상영작으로 출력
    '''
    movies = Movie.objects.all().filter(release_date__range=[date.today() - timedelta(days=30), date.today()])
    if len(movies) >= 10:
        movies = random.sample(list(movies), 10)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def movie_history(request, movie_pk):
    '''
    영화 상세 정보를 클릭하거나 좋아요를 누를 때 해당 로그를 기록하는 함수
    [의문사항]: 1:N과 N:M의 관계가 아닌 단순히 유저 정보와 영화 정보를 기록하는 것이라 데이터의 양이 많아진다. -> DB의 효율적 저장을 생각해봐야한다.
    '''
    movie = get_object_or_404(Movie, movie_id=movie_pk)
    serializer = MovieListSerializer(movie)
    genres = serializer.data['genres']
    if request.method == 'POST':
        user = request.user
        for genre in genres:
            History.objects.create(
                user_id = user.id,
                movie_id = movie_pk,
                genres = genre,
                score = 1
            )
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def movie_list(request):
    '''
    단순히 영화 모든 정보를 나열하는 함수
    [문제사항]: 3000여개의 영화 데이터를 한꺼번에 불러오면 5.7초의 로딩 시간이 필요하다.(필요할 때마다 정보를 불러오는 최적화 필요)
    -> 시간 지연을 줄일 필요가 있음
    '''
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    # print(serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, movie_pk):
    '''
    상세 영화 정보 출력
    '''
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    # print(serializer.data)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def movie_like(request, movie_pk):
    '''
    영화에 대한 좋아요를 눌렀을 때 DB에 대한 저장을 하고 좋아요 취소를 눌렀을 때에는 DB에서 삭제 진행
    '''
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    # 초반 좋아요 정보를 들고와서 화면에 보여주기 위해 활용
    if request.method == 'GET':
        liked = True
        if user in movie.like_users.all():
            liked = True
        else:
            liked = False
        return Response({'liked': liked})
    elif request.method == 'POST':
        if user in movie.like_users.all():
            movie.like_users.remove(user)
            data = {'liked': False}
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        else:
            movie.like_users.add(user)
            data = {'liked': True}
            return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def movie_trend(request):
    '''
    모든 유저들의 History 기록을 탐색해서 일주일 동안 가장 많은 조회수와 좋아요를 얻은 영화를 10개 출력
    [어려운 점]: QuerySet의 활용과 정보 가공이 까다로웠다.
    '''
    movie_dict = {}
    trends = History.objects.filter(updated_at__gte = timezone.now() - timedelta(days=7))
    for trend in trends:
        movie = trend.movie_id
        if movie in movie_dict:
            movie_dict[movie] += 1
        else:
            movie_dict[movie] = 1

    li = []
    for j in movie_dict.items():
        li.append(j)
    li.sort(key=lambda x: x[1], reverse=True)
    total_li = []
    cnt = 0
    for k in li:
        trend_movie = Movie.objects.get(movie_id=k[0])
        total_li.append(trend_movie)
        cnt += 1
        if cnt == 10:
            break
    serializer = MovieListSerializer(total_li, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def movie_recommend(request):
    '''
    [알고리즘 추천]
    
    로그인한 유저를 대상으로 추천 영화를 제공
    해당 유저의 최근 100회의 활동 기록(History Table)을 통해 가장 선호받은 장르 2개를 선정한다.
    
    고정적이지 않고 동적인 영화 추천을 제공하기 위해 3/1의 확률로 3가지의 추천을 제공한다.(장르 2개 한정)
    1. 단순히 평점순을 나열하여 10개의 데이터를 제공
    
    2. 해당 장르에 대해 랜덤으로 10개 추출하여 제공
    
    3. 최신 영화(31일 이내)의 영화를 10개 랜덤 추출하여 제공
    
    '''
    user = request.user
    actions = History.objects.all().filter(user_id=user.id)
    length = actions.count()
    if length == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    if length > 100:
        actions = actions[length-100:]

    genre = {}
    dict1 = actions.values()
    for movie in dict1:
        gen = movie['genres']
        if gen in genre:
            genre[gen] += 1
        else:
            genre[gen] = 1
    li = []
    for i in genre.items():
        li.append(i)
    li.sort(key=lambda x : x[1], reverse=True)
    
    
    if len(li) == 1:
        num = list(range(1, 4))
        getNum = random.sample(num, 1)[0]
        if getNum == 1:     # 평점순 랜덤
            queryset = Movie.objects.filter(genres=li[0][0]).order_by('-vote_average').distinct()[:10]
        elif getNum == 2:   # 올 랜덤
            queryset = Movie.objects.filter(genres=li[0][0]).order_by('?')[:10]
        else:               # 최신영화 중에서 랜덤
            queryset = Movie.objects.filter(genres=li[0][0]).filter(release_date__range=[date.today() - timedelta(days=31), date.today()]).order_by('?')[:10]

    else:
        num = list(range(1, 4))
        getNum = random.sample(num, 1)[0]
        if getNum == 1:     # 평점순 랜덤
            queryset = Movie.objects.filter(genres__in=[li[0][0], li[1][0]]).order_by('-vote_average').distinct()[:10]
        elif getNum == 2:   # 올 랜덤
            movies = Movie.objects.filter(genres__in=[li[0][0], li[1][0]]).values('movie_id').order_by('-vote_average').distinct()
            random_movies = Movie.objects.filter(movie_id__in=movies)
            queryset = random.sample(list(random_movies), 10)
        else:               # 최신영화 중에서 랜덤
            movies = Movie.objects.filter(release_date__range=[date.today() - timedelta(days=365), date.today()]).filter(genres__in=[li[0][0], li[1][0]]).values('movie_id').order_by('-vote_average').distinct()
            random_movies = Movie.objects.filter(movie_id__in=movies)
            queryset = random.sample(list(random_movies), 10)
    serializer = MovieSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def movie_follow_like(request, user_id):
    '''
    [알고리즘 추천]
    
    로그인한 유저가 팔로우한 유저들을 대상으로 영화를 추천해준다.
    팔로우한 유저들이 좋아요를 누른 영화를 파악하여 해당 영화들 중에서 10개를 랜덤으로 제공
    [목적]: 단순히 많은 관심을 받은 영화를 추천하는 게 아니라 동적인 효과를 위해 랜덤을 선택!!
    '''
    User = get_user_model()
    user = User.objects.get(id=user_id) # 나의 정보
    my_like_movies = user.like_movies.all()
    following_people = user.followings.all()
    li = []

    # 내가 팔로우 한 사람들이 좋아하는 영화들의 집합
    for following in following_people:
        movies = following.like_movies.all()
        # print(movies)
        for movie in movies:
            if movie not in li:
                li.append(movie)
    # print(li)
    result = []
    for i in li:
        if i not in my_like_movies:
            result.append(i)
    if len(result) > 10:
        new_result = random.sample(result, 10)
    else:
        new_result = random.sample(result, len(result))

    serializer = MovieSerializer(new_result, many=True)
    # print(serializer.data)
    return Response(serializer.data)



@api_view(['GET'])
def cast_list(request, movie_pk):
    '''
    영화와 관련된 배우, 감독 정보를 추출
    인물 정보를 확인할 수 있는 URL도 포함되어 있다.
    '''
    casts = get_list_or_404(Cast, movie_id=movie_pk)
    serializer = CastSerializer(casts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_genre(request):
    '''
    N대 M 관계를 풀어내기 위해 장르 정보 추출
    '''
    genres = get_list_or_404(Genre)
    serializer = GenreListSerializer(genres, many=True)
    # print(serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
def movie_like_list(request, username):
    '''
    로그인한 유저가 좋아요를 누른 영화가 프로필 화면에 출력될 수 있도록 해주는 함수
    '''
    User = get_user_model()
    user_id = User.objects.get(username=username).pk
    user = get_object_or_404(User, pk=user_id)
    movies = user.like_movies.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_search(request, inputData):
    '''
    [검색 엔진]
    영화 제목과 배우 정보(영문)를 입력하면 해당 영화가 추출되도록 진행
    '''
    movies = Movie.objects.filter(title__contains=inputData)
    movies = list(movies)
    casts = Cast.objects.filter(name__contains=inputData)
    
    for cast in casts:
        movie = Movie.objects.get(movie_id = cast.movie_id)
        if movie not in movies:
            movies.append(movie)

    # overview_movies = Movie.objects.filter(overview__contains=inputData)
    # for oveerview_movie in overview_movies:
    #     if oveerview_movie not in movies:
    #         movies.append(oveerview_movie) 
    # print(li)
    # print(list(movies) + li)
    
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_related(request, movie_id):
    movie = Movie.objects.get(movie_id=movie_id)
    li = movie.genres.all()
    movies = Movie.objects.filter(recommend_movie_id=movie_id).order_by('?')[:6]
    if not(movies):
        if len(li) == 1:
            queryset = Movie.objects.filter(genres__in=[li[0]]).exclude(movie_id__in=[movie_id])
            movies = queryset.order_by('?')[:6]
        else:
            queryset = Movie.objects.filter(genres__in=[li[0],li[1]]).exclude(movie_id__in=[movie_id]).order_by('id').distinct()
            movies = set()
            for movie in queryset:
                if movie not in movies:
                    movies.add(movie)
            movies = random.sample(list(movies), 6)
    serializer = MovieSerializer(movies, many=True)
    # print(serializer)
    return Response(serializer.data)
    


@api_view(['GET'])
def movie_poster(request, movie_id):
    posters = get_list_or_404(Poster, movie_id = movie_id)
    serializer = PosterSerializer(posters, many=True)
    return Response(serializer.data)

# Create your views here.
# def get_movie_data(self):
#     # json 파일 불러오기
#     # 장르에 대한 정보 불러오기
#     genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key=<API_KEY>&language=ko-KR'
#     res2 = requests.get(genre_url)
#     other = res2.json()
#     # print(other['genres'])
#     for genre in other['genres']:
#         Genre.objects.create(
#                 name = genre['name'],
#                 pk = genre['id']
#             )

#     save = []
#     page = 1
#     # 페이지 설정
#     while page < 35:
#         # save 리스트에 영화 정보 저장
#         url = f'https://api.themoviedb.org/3/movie/top_rated?api_key=<API_KEY>&page={page}&language=ko'
#         response = requests.get(url)
        
#         data = response.json()
#         save.extend(data['results'])
#         # print(save)
        
#         # 현재 상영작
#         url_upcoming = f'https://api.themoviedb.org/3/movie/upcoming?api_key=<API_KEY>&language=ko-KR&page={page}'
#         response = requests.get(url_upcoming)
        
#         data_upcoming = response.json()
#         save.extend(data_upcoming['results'])
#         page += 1

    
#     total_movie_id = set()
#     # 각각의 영화 정보를 통해 배우 및 video link 추출
#     for row in save:
        
#         movie_id=row['id']
#         if movie_id in total_movie_id:
#             continue
#         total_movie_id.add(movie_id)
        
#         url_video = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=<API_KEY>'
#         res = requests.get(url_video)
#         other_data = res.json()

#         video_url = 'http://www.youtube.com/embed/'
#         try:
#             video_url += other_data['results'][0]['key']
#         except:
#             # video link가 존재하지 않으면 넘어가기
#             continue
        
#         url_video_image = f'https://api.themoviedb.org/3/movie/{movie_id}/images?api_key=<API_KEY>'
#         res = requests.get(url_video_image)
#         other_data_image = res.json()
#         image = []
#         i = 1
#         for other in other_data_image['backdrops']:
#             image.append(other)
            
#             i += 1
#             if i > 5:
#                 break
        
        
        
#         for i in image:
#             file_path = i['file_path']
#             image_url = f'https://www.themoviedb.org/t/p/original/{file_path}'
#             Poster.objects.create(
#                 movie_id=movie_id,
#                 file_path = image_url,
#             )
            
        
        
        
#         Movie.objects.create(
#         movie_id=row['id'],
#         title = row['title'],
#         poster_path = row['poster_path'],
#         release_date = row['release_date'],
#         overview = row['overview'],
#         video_path = video_url,
#         vote_average = row['vote_average'],
#         recommend_movie_id = 0,
#         )
#         movie = Movie.objects.get(movie_id=movie_id)
#         # print('######################################')
#         # print(movie)
        
#         provider_url = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key=<API_KEY>'
#         res_provider = requests.get(provider_url)
#         provider_data = res_provider.json()
#         try:
#             provider_link = provider_data['results']['KR']['link']
#             providers = provider_data['results']['KR']['flatrate']
#             for provider_logo_path in providers:
#                 path = provider_logo_path['logo_path']
#                 logo_path = f'https://www.themoviedb.org/t/p/original/{path}'
#                 Provider.objects.create(
#                     provider_link = provider_link,
#                     provider_logo_path = logo_path,
#                     movie = movie,
#                 )
#         except:
#             pass
        
        
#         for genre_id in row['genre_ids']:
#             genre = Genre.objects.get(id=genre_id)
#             movie = Movie.objects.get(movie_id= row['id'])
#             movie.genres.add(genre)


#         # 해당 영화의 배우 및 감독에 대한 정보
#         actor_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=<API_KEY>&language=ko-KR'
#         res1 = requests.get(actor_url)
#         other_data1 = res1.json()
#         # print(other_data1['cast'])
        

#         for cast in other_data1['cast']:
#             cast_id = cast['id']
#             cast_url = f'https://www.themoviedb.org/person/{cast_id}?language=ko-KR'
#             Cast.objects.create(
#                 name = cast['name'],
#                 known_for_department = cast['known_for_department'],
#                 movie_id = other_data1['id'],
#                 credit_id = cast_url,
#             )
        
#         save_recommend = []
#         url_recommend = f'https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key=<API_KEY>&language=ko-KR&page=1'
#         response = requests.get(url_recommend)
        
#         data_recommend = response.json()
#         save_recommend.extend(data_recommend['results'])
#         # print(save)
        
#         #### 추천 영화 #####
#         for row in save_recommend:
#             movie_id_recommend=row['id']
#             if movie_id_recommend in total_movie_id:
#                 continue
#             total_movie_id.add(movie_id_recommend)
            
            
#             url_video = f'https://api.themoviedb.org/3/movie/{movie_id_recommend}/videos?api_key=<API_KEY>'
#             res = requests.get(url_video)
#             other_data = res.json()

#             video_url = 'http://www.youtube.com/embed/'
#             try:
#                 video_url += other_data['results'][0]['key']
#             except:
#                 # video link가 존재하지 않으면 넘어가기
#                 continue
            
#             url_video_image = f'https://api.themoviedb.org/3/movie/{movie_id_recommend}/images?api_key=<API_KEY>'
#             res = requests.get(url_video_image)
#             other_data_image = res.json()
#             image = []
#             i = 1
#             for other in other_data_image['backdrops']:
#                 image.append(other)
                
#                 i += 1
#                 if i > 5:
#                     break
            
#             for i in image:
#                 file_path = i['file_path']
#                 image_url = f'https://www.themoviedb.org/t/p/original/{file_path}'
#                 Poster.objects.create(
#                     movie_id=movie_id_recommend,
#                     file_path = image_url,
#                 )
                
            
#             Movie.objects.create(
#             movie_id=row['id'],
#             title = row['title'],
#             poster_path = row['poster_path'],
#             release_date = row['release_date'],
#             overview = row['overview'],
#             video_path = video_url,
#             vote_average = row['vote_average'],
#             recommend_movie_id = movie_id,
#             )
#             movie = Movie.objects.get(movie_id= row['id'])
            

            
#             provider_url = f'https://api.themoviedb.org/3/movie/{movie_id_recommend}/watch/providers?api_key=<API_KEY>'
#             res_provider = requests.get(provider_url)
#             provider_data = res_provider.json()
#             try:
#                 provider_link = provider_data['results']['KR']['link']
#                 providers = provider_data['results']['KR']['flatrate']
#                 for provider_logo_path in providers:
#                     path = provider_logo_path['logo_path']
#                     logo_path = f'https://www.themoviedb.org/t/p/original/{path}'
#                     Provider.objects.create(
#                         provider_link = provider_link,
#                         provider_logo_path = logo_path,
#                         movie = movie,
#                     )
#             except:
#                 pass
            
            
            
            
            
#             for genre_id in row['genre_ids']:

#                 genre = Genre.objects.get(id=genre_id)
#                 movie = Movie.objects.get(movie_id= row['id'])
#                 movie.genres.add(genre)


#             # 해당 영화의 배우 및 감독에 대한 정보
#             actor_url = f'https://api.themoviedb.org/3/movie/{movie_id_recommend}/credits?api_key=<API_KEY>&language=ko-KR'
#             res1 = requests.get(actor_url)
#             other_data1 = res1.json()
#             # print(other_data1['cast'])
            

#             for cast in other_data1['cast']:
#                 cast_id = cast['id']
#                 cast_url = f'https://www.themoviedb.org/person/{cast_id}?language=ko-KR'
#                 Cast.objects.create(
#                     name = cast['name'],
#                     known_for_department = cast['known_for_department'],
#                     movie_id = other_data1['id'],
#                     credit_id = cast_url,
#                 )
        
        
        

#     return HttpResponse('Success convert json to database')

