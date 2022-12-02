from django.db import models
from django.contrib.auth.models import AbstractUser


# 팔로우, 프로필 이미지 기능을 위한 모델
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    profile_image = models.ImageField(blank=True, upload_to='images/')
