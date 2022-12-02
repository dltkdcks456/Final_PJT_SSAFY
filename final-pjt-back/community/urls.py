from django.urls import path
from . import views

urlpatterns = [
    path('reviews/<int:movie_id>/', views.review_list),
    path('reviews/profile/<int:review_user_id>/', views.review_profile),
    path('reviews/detail/<int:review_id>/', views.review_detail),
    path('reviews/like/<int:review_id>/', views.review_like),
    path('comment/<int:review_id>/', views.comment_list),
    path('comment/detail/<int:comment_id>/', views.comment_detail),
]
