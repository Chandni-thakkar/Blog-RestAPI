from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.blog.models import Post


class BlogApiTests(TestCase):

    def setUp(self):
        """
        Set up the test environment:
        - Create a test user
        - Initialize API client for testing API endpoints
        """
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_post_authenticated(self):
        """
        Test the creation of a post when the user is authenticated
        """
        url = "/api/posts/"  # Adjust with the correct API endpoint for creating posts
        data = {
            "title": "Test Post",
            "body": "This is the body of the test post.",
        }
        response = self.client.post(url, data, format="json")

        # Assert the status code and the content of the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test Post")
        self.assertEqual(response.data["author"], self.user.id)

    def test_create_post_unauthenticated(self):
        """
        Test that an unauthenticated user cannot create a post
        """
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        url = "/api/posts/"
        data = {
            "title": "Test Post",
            "body": "This post should not be created.",
        }
        response = self.client.post(url, data, format="json")

        # Assert that unauthenticated users cannot create a post
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_validate_unique_slug(self):
        """
        Test that a post cannot be created with a non-unique slug
        """
        # Create an initial post
        post = Post.objects.create(
            title="Existing Post",
            slug="existing-post",  # Predefined slug
            body="This is the body of the existing post.",
            author=self.user
        )

        # Try to create a new post with the same slug
        url = "/api/posts/"
        data = {
            "title": "Duplicate Slug Post",
            "slug": "existing-post",  # Same slug as the existing post
            "body": "This should fail due to a duplicate slug.",
        }
        response = self.client.post(url, data, format="json")

        # Assert that the response contains an error about the slug being non-unique
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('slug', response.data)

    def test_post_creation_with_invalid_data(self):
        """
        Test post creation with invalid data (title too short, body too short)
        """
        url = "/api/posts/"
        data = {
            "title": "Sho",  # Title is too short
            "body": "Short",  # Body is too short
        }
        response = self.client.post(url, data, format="json")

        # Assert that the response contains validation errors
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertIn("body", response.data)

