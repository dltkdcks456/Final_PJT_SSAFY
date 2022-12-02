from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from .models import User
from rest_framework import status
from .serializers import UserSerializer
from .forms import UserForm
import random
import shutil


# @api_view(['GET'])
# def default_image(request):
#     ran = random.sample(range(1, 5), 1)
#     image = 'default' + str(ran)
#     img = open(f'media/defaults/{image}.png', 'rb')
#     response = FileResponse(img)
#     return response


@api_view(['GET', 'POST', 'DELETE'])
def profile_image(request, user_id):
    '''
    프로필 이미지를 저장하고 초기화하고 불러오는 함수
    
    [문제사항 1]: 이미지를 저장하면 기존 사진은 지워질 수 있게 구현하는 게 어려웠다. -> POST 요청을 했을 때에는 기존 데이터를 미리 삭제하고 저장하는 쪽으로 해결
     ※ django-cleanup을 활요하려고 하였으나, 기존 프로필을 지워버리는 현상이 발생
     
    [문제사항 2]: default 이미지를 다양한 색으로 표현하고 싶어서 따로 defaults 폴더 내에 기본 프로필 이미지를 색별로 4개 저장해주고 랜덤으로 제공하는 것으로 변경
    
    [문제사항 3]: 가장 초기의 이미지는 default 이미지를 복사해서 파일명에 유저명을 합쳐서 image 폴더 내에 저장(유저별 사진 구분 가능)
    '''
    User = get_user_model()
    me = request.user
    person = User.objects.get(id=user_id)
    if request.method == 'GET':
        if person.profile_image:
            serializer = UserSerializer(person)
        else:
            ran = random.sample(range(0, 4), 1)
            image = './media/defaults/default' + str(ran[0]) + '.png'
            shutil.copy(image, './media/images/default'+ str(ran[0]) + person.username + '.png')
            person.profile_image = 'images/default'+ str(ran[0]) + person.username + '.png'
            person.save()
            serializer = UserSerializer(person)
        return Response(serializer.data)
    elif request.method == 'POST':
        if me == person:
            person.profile_image.delete()
            form = UserForm(request.POST, request.FILES, instance=person)
            # print(form.is_valid())
            # print(request.FILES.get('image'))
            if form.is_valid():
                form = form.save(commit=False)
                form.profile_image=request.FILES.get('image')
                form.save()
                # print(form)
            serializer = UserSerializer(person)
            return Response(serializer.data)
    elif request.method == 'DELETE':
        person.profile_image.delete()
        ran = random.sample(range(0, 4), 1)
        image = './media/defaults/default' + str(ran[0]) + '.png'
        # shutil.copy(image, './media/images/default'+ str(ran[0]) + '.png')
        # person.profile_image = 'images/default'+ str(ran[0]) + '.png'
        shutil.copy(image, './media/images/default'+ str(ran[0]) + person.username + '.png')
        person.profile_image = 'images/default'+ str(ran[0]) + person.username + '.png'
        person.save()
        serializer = UserSerializer(person)
        return Response(serializer.data)
    
# 유저 pk 입력 시 username 반환 기능
# data: {userid: userid}
# headers: {Authorization: Token {token}}
@api_view(['POST'])
def wantname(request):
    '''
    username으로 userid를 뽑아내는 함수
    '''
    Userid = request.user
    if request.method == 'POST':
        user = Userid.id
        userid = request.data['userid']
        username = User.objects.get(pk = userid).username
        return JsonResponse({'username': username, 'userid': user})

# username 입력 시 유저 pk 반환 기능
# data: {username: username}
# headers: {Authorization: Token {token}}
@api_view(['POST'])
def wantid(request):
    '''
    userid를 username으로 뽑아내는 함수
    '''
    if request.method == 'POST':
        username = request.data['username']
        userid = User.objects.get(username = username).pk
        return JsonResponse({'userid': userid})

# 회원 탈퇴
@api_view(['POST'])
def leave(request):
    '''
    회원 탈퇴 시 유저 정보 삭제
    '''
    if request.method == 'POST':
        user = request.user
        # user.is_active = False
        # user.save()
        user.delete()
        return HttpResponse('OK')

# 팔로우
@api_view(['GET', 'POST'])
def follow(request, user_pk):
    '''
    팔로우 버튼을 눌렀을 경우 N대 M 관계를 설정해주는 함수
    '''
    person = get_object_or_404(get_user_model(), pk=user_pk)    # you
    user = request.user                                         # me
    if person != user:
        if request.method == 'GET':
            if person.followers.filter(pk=user.pk).exists():
                return Response(True, status=status.HTTP_201_CREATED)
            else:
                return Response(False, status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'POST':
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
                return Response(False, status=status.HTTP_204_NO_CONTENT)
            else:
                person.followers.add(user)
                return Response(True, status=status.HTTP_201_CREATED)
    return HttpResponse('NO')


@api_view(['GET'])
def following_profile(request, user_pk):
    '''
    팔로잉 유저 정보를 불러오는 함수
    '''
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    followings = person.followings.all()
    serializer = UserSerializer(followings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def follower_profile(request, user_pk):
    '''
    팔로워 유저 정보를 불러오는 함수
    '''
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    followers = person.followers.all()
    serializer = UserSerializer(followers, many=True)
    return Response(serializer.data)



# 팔로워 수 세기
@api_view(['GET'])
def followcount(request, user_pk):
    '''
    팔로잉, 팔로워 수를 제공해주는 함수
    '''
    person = get_object_or_404(get_user_model(), pk=user_pk)
    context = {
        'followers_count': person.followers.count(),
        'followings_count': person.followings.count(),
    }
    # print(person.followers.count())
    # print(person.followings.count())
    return JsonResponse(context)