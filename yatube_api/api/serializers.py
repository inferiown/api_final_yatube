from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

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
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'group', 'comments')
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'slug', 'title', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('id', 'user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return value

#    def validate(self, data):
#        if not self.initial_data.get('following'):
#            raise serializers.ValidationError(
#                'Переменная following не передана в запросе')
#
#        request = self.context.get('request')
#        following = self.initial_data.get('following')
#
#        if not User.objects.filter(username=following).exists():
#            raise serializers.ValidationError(
#                'Такого пользователя не существует')
#
#        author = User.objects.get(username=following)
#        if author == request.user:
#            raise serializers.ValidationError(
#                'Нельзя подписаться на самого себя')
#
#        if Follow.objects.filter(following=author,
#                                 user=request.user).exists():
#            raise serializers.ValidationError(
#                'Вы уже подписаны на данного автора')
#        return data
