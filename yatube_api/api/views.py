from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post, Follow, User
from .permissions import AuthorOrReadOnly
from .serializers import (CommentSerializer, GroupSerializer,
                          PostSerializer, FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AuthorOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        new_queryset = post.comments.all()
        return new_queryset


class FollowViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username')





#    def perform_create(self, serializer):
#        author_username = serializer.data.get('following')
#        author = get_object_or_404(User, username=author_username)
#        serializer.save(following=author, user=self.request.user)
#        following = serializer.data.get('following')
#        user = self.request.user
#        author = get_object_or_404(User, user=following)
#        serializer.save(user=user, author=author)

#    def get_queryset(self):
#        user = get_object_or_404(User, user=self.request.user)
#        new_queryset = user.following.all()
#        return new_queryset
