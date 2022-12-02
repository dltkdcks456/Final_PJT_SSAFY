from django.urls import path
from . import views

urlpatterns = [
    # 유저 pk로 아이디 뽑기, 유저 아이디로 pk뽑기
    path('leave/', views.leave, name='leave'),
    path('follow/<int:user_pk>/', views.follow, name='follow'),
    path('following/profile/<int:user_pk>/', views.following_profile, name='following_profile'),
    path('follower/profile/<int:user_pk>/', views.follower_profile, name='follower_profile'),
    path('followcount/<int:user_pk>/', views.followcount, name='followcount'),
    path('wantname/', views.wantname, name='wantname'),
    path('wantid/', views.wantid, name='wantid'),
    path('profile_image/<int:user_id>/', views.profile_image),
    # path('default_image/', views.default_image),
]