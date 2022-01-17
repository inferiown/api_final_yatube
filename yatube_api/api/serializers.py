from rest_framework import serializers
from rest_framework import status
from rest_framework.relations import SlugRelatedField
from rest_framework.exceptions import ParseError
from django.shortcuts import get_object_or_404


from posts.models import Comment, Follow, Group, Post, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('__all__')


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
#    comments = SlugRelatedField(many=True, read_only=True, slug_field='text')
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'group', 'comments')
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'slug', 'title', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.StringRelatedField()

    class Meta:
        model = Follow
        fields = ('id', 'user', 'following')

    def create(self, validated_data):
        request = self.context.get('request')
        following = self.initial_data.get('following')

        if not self.initial_data.get('following'):
            raise ParseError(
                detail="No following variable provided",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not User.objects.filter(username=following).exists():
            raise ParseError(
                detail="such user doesn't exist",
                code=status.HTTP_400_BAD_REQUEST,
            )

        author = get_object_or_404(User,
                                   username=following)
        user = get_object_or_404(User,
                                 username=request.user.username)
        if author == request.user:
            raise ParseError(
                detail="User can't follow himself",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if Follow.objects.filter(following=author,
                                 user=request.user).exists():
            raise ParseError(
                detail="User can't follow same author twice",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return Follow.objects.create(user=user, following=author)
