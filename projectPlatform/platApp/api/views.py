# views.py

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import generics

from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.db.models import Q
from platApp.utils import calculate_sentiment

from platApp.serializer import *
from ..models import *
import os


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''
        Serializer for token
    '''
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    '''
        Gets the token for the user
    '''
    serializer_class = MyTokenObtainPairSerializer


class UserCreateAPIView(CreateAPIView):
    '''
        Creates a user
    '''
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    '''
        Gets the profile of the user
    '''    
    user = request.user
    profile = user.profile
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_user_profile(request):
    '''
        Posts the profile of the user
    '''    
    user = request.user
    profile = user.profile
    profile.biography = request.data['biography']
    profile.save()
    return Response({'Success': 'Profile updated'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_img(request):
    '''
        Gets the profile image of the user
    '''    
    user = request.user
    profile = user.profile
    photo = profile.photo
    return FileResponse(photo, content_type='image/jpg')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_profile_img(request):
    '''
        Post profile image of the user
    '''    
    user = request.user
    profile = user.profile

    filename = f'{user.username}.jpg'
    photo = request.data['photo']
    destination = os.path.join(settings.MEDIA_ROOT, 'img', filename)

    with open(destination, 'wb') as destination:
        for chunk in photo.chunks():
            destination.write(chunk)

    profile.photo = f'img/{filename}'
    profile.save()
    
    return Response({'Success': 'Profile image updated'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_following(request, username):
    '''
        Gets the followers of the user
    '''    
    user = request.user
    followed = User.objects.get(username=username)

    # Returns whether the user is following the user using true/false
    isFollowing = Followers.objects.filter(user=user, followed=followed).exists()
    return Response({'Status': isFollowing}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_follower(request, username):
    '''
        Actually POST's a follower
    '''
    user = request.user
    followed = User.objects.get(username=username)

    # If the user is already following the user, delete the entry
    if Followers.objects.filter(user=user, followed=followed).exists():
        follower_entry = Followers.objects.get(user=user, followed=followed)
        follower_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Otherwise, create a new entry
    Followers.objects.create(user=user, followed=followed)
    return Response(status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
def get_search_results(request, username):
    '''
        Search
    '''
    user = User.objects.filter(Q(username__icontains=username) | Q(last_name__icontains=username)) # case-sensitive filtering by username with many=true
    post = Post.objects.filter(Q(title__icontains=username) | Q(content__icontains=username))

    serializer_user = UserSerializer(user, many=True)
    serializer_post = PostSerializer(post, many=True)

    response_data = {
        'users': serializer_user.data,
        'posts': serializer_post.data
    }
    return Response(response_data)


@api_view(['GET'])
def get_public_user_profile(request, username):
    '''
        Gets the public user profile
    '''
    if (request.user and request.user.username == username):
        return Response({'Location': '/profile'}, status=status.HTTP_302_FOUND)
    user = User.objects.get(username=username)
    if not user:
        return Response({'Error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PublicProfileSerializer(user.profile)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_public_user_profile_img(request, username):
    '''
        Gets the public user profile image
    '''    
    user = User.objects.get(username=username)
    profile = user.profile
    photo = profile.photo
    return FileResponse(photo, content_type='image/jpg')


@api_view(['GET'])
def get_public_user_profile_posts(request, username):
    '''
        Gets the public user profile posts
    '''
    user = User.objects.get(username=username)
    id = user.id

    posts = Post.objects.filter(author_id=id)
    serializer = PublicProfilePostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_posts(request):
    '''
        Gets all posts in database
    '''    
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    '''
        Creates a post
    '''    
    user = request.user
    post = Post(author=user)
    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post(request, post_id):
    '''
        Gets a specific post
    '''   
    try:
        parent_post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'Error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    post_serializer = PostSerializer(parent_post, many=False)

    return Response(post_serializer.data)


@api_view(['DELETE'])
def delete_post(request, post_id):
    '''
        Deletes a post
    '''    
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'Error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    post.delete()
    return Response({'Success': 'Post deleted'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_comment(request, comment_id):
    '''
        Gets a specific comment
    '''    
    try:
        parent_post = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({'Error': 'Comment not found'},status=status.HTTP_404_NOT_FOUND)
    comment_serializer = CommentSerializer(parent_post, many=False)

    return Response(comment_serializer.data)


@api_view(['GET'])
def get_comment_on_post(request, post_id):
    '''
        Gets all comments on a specific post
    '''    
    try:
        parent_post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'Error': 'Post not found'},status=status.HTTP_404_NOT_FOUND)
    try:
        comments = Comment.objects.filter(post=parent_post, parent = None)
    except:
        return Response({'Post': comments_serializer.data, 'Comments': []}, status=status.HTTP_200_OK)
    comments_serializer = CommentSerializer(comments, many=True)

    return Response(comments_serializer.data)


@api_view(['GET'])
def get_subComments(request, comment_id):
    '''
        Gets comments on a specific comment
    '''    
    try:
        parent_comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({'Error': 'Comment not found'},status=status.HTTP_404_NOT_FOUND)
    try:
        comments = Comment.objects.filter(parent=parent_comment)
    except:
        return Response({'Comment': comments_serializer.data, 'Comments': []}, status=status.HTTP_200_OK)
    comments_serializer = CommentSerializer(comments, many=True)

    return Response(comments_serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    '''
        Creates a comment on a post
    '''    
    post_id = request.data['post']
    user = request.user
    try:
        parent_post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'Error': 'Post not found'},status=status.HTTP_404_NOT_FOUND)
    comment = Comment(post=parent_post, author=user)
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_on_comment(request):
    '''
        Creates a comment on a specific comment
    '''    
    parent_id = request.data['parent']
    user = request.user
    try:
        parent_comment = Comment.objects.get(id=parent_id)
    except Comment.DoesNotExist:
        return Response({'Error': 'parent comment not found'},status=status.HTTP_404_NOT_FOUND)
    
    comment = Comment(parent=parent_comment, author=user, post=parent_comment.post)
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_reaction(request, post_id):
    """
        Get user reaction to a post and the total reactions and comments count
    """

    user = request.user
    try:
        reaction_post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        reaction = Reaction.objects.get(user=user, post=reaction_post)
        serializer = ReactionSerializer(reaction)
        user_reaction_data = serializer.data
    except Reaction.DoesNotExist:
        user_reaction_data = None

    # Count the total reactions for the post
    total_reactions_count = Reaction.objects.filter(post=reaction_post).count()
    
    sentiment = calculate_sentiment(reaction_post)

    # Count the total comments for the post
    total_comments_count = Comment.objects.filter(post=reaction_post).count()
    return Response({
        'user_reaction': user_reaction_data,
        'total_reactions_count': total_reactions_count,
        'total_comments_count': total_comments_count,
        'sentiment': sentiment,
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_reaction(request, post_id):
        
    """
        Delete a user's reaction to a post and update the total reactions count
    """
    user = request.user
    try:
        reaction_post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        reaction = Reaction.objects.get(user=user, post=reaction_post)
        reaction.delete()
        # Count the total reactions for the post
        total_reactions_count = Reaction.objects.filter(post=reaction_post).count()
    
        sentiment = calculate_sentiment(reaction_post)

        # Count the total comments for the post
        total_comments_count = Comment.objects.filter(post=reaction_post).count()
        return Response({
        'user_reaction': None,
        'total_reactions_count': total_reactions_count,
        'total_comments_count': total_comments_count,
        'sentiment': sentiment,
    }, status=status.HTTP_200_OK)
    
    except Reaction.DoesNotExist:
        return Response({'message': 'No reaction found'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def react_to_post(request, post_id):
    """
    React to a post, delete if the same reaction is sent as post,
    and update if there is a new reaction to a already reacted to post,
      and update the total reactions count
    """
    req_user = request.user

    try:
        reaction_post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    total_comments_count = Comment.objects.filter(post=reaction_post).count()   
 
    try:
        # check if the user has already reacted to the post
        reaction = Reaction.objects.get(user=req_user, post=reaction_post)
        if reaction.type == request.data['type']:
            # delete reaction if the user reacts with the same type
            reaction.delete()
            # update reaction count
            total_reactions_count = Reaction.objects.filter(post=reaction_post).count()
            sentiment = calculate_sentiment(reaction_post)
            return Response({
                'user_reaction': None,
                'total_reactions_count': total_reactions_count,
                'total_comments_count': total_comments_count,
                'sentiment': sentiment,
                }, status=status.HTTP_200_OK)
        else:
            # update reaction type
            reaction.type = request.data['type']
            reaction.save()
            serializer = ReactionSerializer(reaction)
            # update reaction count
            total_reactions_count = Reaction.objects.filter(post=reaction_post).count()
            sentiment = calculate_sentiment(reaction_post)
            return Response({
                'user_reaction': serializer.data,
                'total_reactions_count': total_reactions_count,
                'total_comments_count': total_comments_count,
                'sentiment': sentiment,
                }, status=status.HTTP_200_OK)
        
    except Reaction.DoesNotExist:
        # create new reaction
        reaction = Reaction(user=req_user, post=reaction_post, type = request.data['type'])
        reac_data = {'user': req_user.id, 'post': reaction_post.id, 'type': request.data['type']}
        serializer = ReactionSerializer(reaction, data=reac_data)
        if serializer.is_valid():
            serializer.save()
            # update reaction count
            total_reactions_count = Reaction.objects.filter(post=reaction_post).count()
            sentiment = calculate_sentiment(reaction_post)
            return Response({
                'user_reaction': serializer.data,
                'total_reactions_count': total_reactions_count,
                'total_comments_count': total_comments_count,
                'sentiment': sentiment,
                }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryList(generics.ListAPIView):
    """
        Fetches all categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagList(generics.ListAPIView):
    """
        Fetches all tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

