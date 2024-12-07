from rest_framework import serializers
from .models import Post, Comment
from apps.authentication.models import CustomUser

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [ 'title', 'slug', 'body','author']
        read_only_fields = ['author']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate_body(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Body must be at least 10 characters long.")
        return value
class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())  # This ensures only valid post IDs can be passed

    class Meta:
        model = Comment
        fields = [ 'id','body','post','author']
        read_only_fields = ['author']
