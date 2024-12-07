from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from apps.authentication.models import BaseModel, CustomUser

class Post(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Automatically generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        # Perform custom validation
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def clean(self):
        # Validate title length
        if len(self.title) < 5:
            raise ValidationError('Title must be at least 5 characters long.')

        # Validate body length (optional)
        if len(self.body) < 10:
            raise ValidationError('Body must be at least 10 characters long.')

        # Validate uniqueness of slug
        if Post.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            raise ValidationError('Slug must be unique.')

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['author']),
        ]


class Comment(BaseModel):
    body = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"

    def clean(self):
        # Validate comment length
        if len(self.body) < 5:
            raise ValidationError('Comment must be at least 5 characters long.')

    class Meta:
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['author']),
        ]

