from rest_framework import serializers
from .models import Review, Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', 'comment_user',)


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        exclude = ('like_users',)
        read_only_fields = ('movie', 'review_user',)

