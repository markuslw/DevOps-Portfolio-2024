#urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    
    #
    #   User profile
    #
    # gets the profile of the user
    path('profile/', views.get_profile),
    # gets the profile image of the user
    path('profile/img', views.get_profile_img),
    # lets the user upload a profile image
    path('profile/img/upload', views.post_profile_img),
    # lets the user update their profile
    path('profile/upload', views.post_user_profile),
    
    #
    #   Sign in and sign up, auth tokens
    #
    path('users/', views.UserCreateAPIView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #
    #   Public user profile
    # gets a public user's profile (search result so less data fetching)
    path('search/<str:username>/', views.get_search_results, name='get_search'),
    # gets a public user's profile
    path('username/<str:username>/', views.get_public_user_profile, name='get_public_user'),
    # posts a follow
    path('username/<str:username>/follow', views.post_follower, name='post_follower'),
    # gets follow status
    path('username/<str:username>/isfollowing', views.is_following, name='is_following'),
    # gets a public user's profile image
    path('username/<str:username>/img', views.get_public_user_profile_img, name='get_public_user_profile_img'),
    # gets a public user's posts
    path('username/<str:username>/posts', views.get_public_user_profile_posts, name='get_public_user_profile_posts'),

    #
    #   Posts
    #
    # the public url for a post through a user and the id
    path('username/<str:username>/post/<int:post_id>', views.get_post, name='get_post'),
    # endpoint for a post directly through the post id
    path('post/<int:post_id>/', views.get_post, name='get_post'),
    # endpoint for deleting a post
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    # endpoint for creating a post
    path('post/create/', views.create_post, name='create_post'),
    # endpoint for getting all posts in database
    path('post/all/', views.get_all_posts, name='get_all_posts'),
    # endpoint for getting multiple comments on a post
    path('post/comment/<int:post_id>/', views.get_comment_on_post, name = 'get_comment_on_post'),

    #
    #   Comments
    #
    # the public url for getting a specific comment through a user and the id
    path('username/<str:username>/comment/<int:comment_id>/', views.get_comment, name='get_comment'),
    # the endpoint for getting a specific comment directly through the comment id
    path('comment/<int:comment_id>/', views.get_comment, name='get_comment'),
    # endpoint for creating a comment on a post
    path('comment/create/', views.create_comment, name = 'create_comment'),

    #
    #   SubComments
    #
    # Gets a spesific subcomment
    path('subComments/<int:comment_id>/', views.get_subComments, name = 'get_subComments'),
    # Gets the comments made on a comment
    path('subComments/', views.comment_on_comment, name = 'comment_on_comment'),
    
    #
    #   tags and categories
    #
    # Fetches all categories
    path('categories/', CategoryList.as_view(), name='category_list'),
    # Fetches all tags
    path('tags/', TagList.as_view(), name='tag_list'),
    #
    #
    #
    #
    #   Reactions
    #
    # fetches number of reactions and comments on a post, and checks if the user has reacted to the post
    path('posts/get_reaction/<int:post_id>/', views.get_user_reaction, name='get_user_reaction'),
    # deletes a user's reaction to a post
    path('posts/remove_reaction/<int:post_id>/', views.delete_user_reaction, name='delete_user_reaction'),
    # reacts to a post, updates a reaction, or deletes a reaction if the user has already reacted with the same reaction
    path('posts/react/<int:post_id>/', views.react_to_post, name='react_to_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
