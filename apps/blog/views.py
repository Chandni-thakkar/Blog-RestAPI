from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        # Automatically set the author to the current user
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Fetch top 5 posts with the most comments
        if self.request.query_params.get('top_posts'):
            return Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:5]
        return Post.objects.all()

    def retrieve(self, request, *args, **kwargs):
        post = self.get_post_by_slug(kwargs.get('slug'))
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        post = self.get_post_by_slug(kwargs.get('slug'))
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        post = self.get_post_by_slug(kwargs.get('slug'))
        post.delete()
        return Response(status=204)

    def get_post_by_slug(self, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found.")

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = self.get_post_from_data(serializer.validated_data)
        # Automatically set the author and post fields
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_slug = self.kwargs.get('slug')
        if post_slug:
            return Comment.objects.filter(post__slug=post_slug)
        return Comment.objects.all()

    def list(self, request, *args, **kwargs):
        post = self.get_post_by_slug(kwargs.get('slug'))
        comments = Comment.objects.filter(post=post)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        post = self.get_post_by_slug(kwargs.get('slug'))
        request.data['post'] = post.id
        request.data['author'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def get_post_by_slug(self, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found.")

    def get_post_from_data(self, data):
        post_id = data.get('post')
        try:
            return Post.objects.get(id=post_id.id)
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found.")
