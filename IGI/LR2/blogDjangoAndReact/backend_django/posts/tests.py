from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient
from rest_framework import status
from .models import Post, Image
from genres.models import Genre

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token


def create_genre(genre_data):
    """
    Create a genre with the given `genre_data` dictionary
    """

    return Genre.objects.create(**genre_data)


def create_post(post_data):
    """
    Create a post with the given `post_data` dictionary
    """

    return Post.objects.create(**post_data)


def create_image(image_data):
    """
    Create a Image with the given `post_data` dictionary
    """

    return Image.objects.create(**image_data)


def create_user(username, email, password):
    """
    Create a user with the given parameters
    """

    return User.objects.create_user(username, email, password)


class PostsTest(APITestCase):

    def set_new_objects(self):
        """
        Ensure we can create a new object.
        """

        username = 'paula'
        email = 'paula@gmail.com'
        password = 'mypasswprd123'

        user = create_user(username, email, password)

        client = APIClient()

        # https://stackoverflow.com/q/31283611/9655579
        response = client.post("api/token/", {"username": username, "password": password},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response_content["token"]

        genre_data = {
            'name': 'Movies',
            'slug':'movies',
            'description':   'description of Movies',
            'show_menu_list':'YES'
        }

        genre = create_genre(genre_data)

        post_data = {
            'title': 'Spiderman 3',
            'slug':'spiderman',
            'description':   'description of spiderman',
            'status': 1,
            'country':'US',
            'image_post':'posts/2f474f0e-1168-4f00-b123-2556c30cf385.jpg',
            'author_id': user.id
        }

        post = create_post(post_data)
        post.genres.add(genre)

        post_data = {
            'title': 'Spiderman 3',
            'slug':'spiderman',
            'description':   'description of spiderman',
            'status': 1,
            'country':'US',
            'image_post':'posts/2f474f0e-1168-4f00-b123-2556c30cf385.jpg',
            'author_id': user.id
        }

        post = create_post(post_data)

        image_data = {
            'post': post.id,
            'image_post':'posts/56023637-a604-4857-8053-ae2c9ad4c2b9.jpg',
        }

        image = create_image(image_data)

        comment_data = {
            'post': 'Spiderman 3',
            'author':user.id,
            'content': 'My comment'
        }

        response = self.client.post("api/comments", comment_data, Authorization='JWT ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_genres_get_endpoint(self):

        url = reverse('genres:genres')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_posts_get_endpoint(self):

        url = reverse('posts:posts')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_featured_posts_get_endpoint(self):

        url = reverse('posts:featured_posts')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# https://www.django-rest-framework.org/api-guide/testing/#example_1
# https://docs.djangoproject.com/en/3.1/intro/tutorial05/#testing-the-detailview