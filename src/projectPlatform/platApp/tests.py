from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from platApp.models import Post, Profile, Reaction, Comment
from rest_framework_simplejwt.tokens import RefreshToken

class ViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user)
        self.token = self.get_jwt_token(self.user)

        # Creating sample post
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def auth_headers(self):
        return {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}


    """
        Test to see if the user can get their profile.
    """
    def test_get_all_posts(self):
        response = self.client.get(reverse('get_all_posts'), **self.auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    """
        Test to see if the user can create a post.
    """
    def test_create_post(self):
        post_data = {
            'title': 'New Post',
            'content': 'New Content',
            'tags': [],
            'category': None
        }
        response = self.client.post(reverse('create_post'), post_data, content_type='application/json', **self.auth_headers())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """
            Test to see if the user can get a spesific post.        
        """
    def test_get_post(self):
        response = self.client.get(reverse('get_post', args=[self.post.id]), **self.auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """
            Test to see if the user can delete a post.
        """
    def test_delete_post(self):
        response = self.client.delete(reverse('delete_post', args=[self.post.id]), **self.auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        """
            Test to see if the user can get all comments on a post.
        """
    def test_get_comment_on_post(self):
        # Create a comment on the post
        comment = Comment.objects.create(post=self.post, author=self.user, content='Test Comment')
        response = self.client.get(reverse('get_comment_on_post', args=[self.post.id]), **self.auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
        Test to see if the user can create a comment.
    """
    def test_create_comment(self):
        comment_data = {
            'post': self.post.id,
            'content': 'Test Comment'
        }
        response = self.client.post(reverse('create_comment'), comment_data, content_type='application/json', **self.auth_headers())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
        """
            Test to see if the user can create a reply to a comment.
        """
    def test_create_comment_reply(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Test Comment')
        comment_data = {
            'post': self.post.id,
            'content': 'Test Reply',
            'parent': comment.id
        }
        response = self.client.post(reverse('create_comment'), comment_data, content_type='application/json', **self.auth_headers())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    """
        Get the user reaction to a post.
    """
    def test_get_user_reaction(self):
        reaction = Reaction.objects.create(user=self.user, post=self.post, type='like')
        response = self.client.get(reverse('get_user_reaction', args=[self.post.id]), **self.auth_headers())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_reaction"]["type"], 'like')

    """
        Test to see if the user can react to a post.
    """
    def test_react_to_post(self):
        react_data = {
            'type': 'like'
        }
        response = self.client.post(reverse('react_to_post', args=[self.post.id]), react_data, content_type='application/json', **self.auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_reaction"]["type"], 'like')
    
    """
        Test to see if the user can update their reaction to a post.
    """
    def test_update_user_reaction(self):
        reaction = Reaction.objects.create(user=self.user, post=self.post, type='like')
        react_data = {
            'type': 'dislike'
        }
        response = self.client.post(reverse('react_to_post', args=[self.post.id]), react_data, content_type='application/json', **self.auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_reaction"]["type"], 'dislike')
    
    """
        Test to see if the user can delete their reaction to a post, by reacting with the same type again.
    """
    def test_delete_user_reaction_v1(self):
        reaction = Reaction.objects.create(user=self.user, post=self.post, type='like')
        react_data = {
            'type': 'like'
        }
        response = self.client.post(reverse('react_to_post', args=[self.post.id]), react_data, content_type='application/json', **self.auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_reaction"], None)

        """
            Test the delete_user_reaction endpoint.
        """
    def test_delete_user_reaction_v2(self):
        reaction = Reaction.objects.create(user=self.user, post=self.post, type='like')
        response = self.client.delete(reverse('delete_user_reaction', args=[self.post.id]), **self.auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_reaction"], None)
