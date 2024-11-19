# serializer.py

from rest_framework import serializers
from platApp.models import *
from django.contrib.auth import get_user_model

# serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

class FollowersSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    followed = serializers.CharField(source='followed.username', read_only=True)

    class Meta:
        model = Followers
        fields = '__all__'

class SearchProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'user.username']

class PublicProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'photo', 'username']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer(required=False)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = get_user_model().objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        if profile_data:
            Profile.objects.create(user=user, **profile_data)

        return user

    class Meta:
        model = User
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'tags', 'category', 'created_at', 'updated_at']

    
class PublicProfilePostSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
    
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'updated_at']


# Reaction serializer for likes/dislikes on posts.
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'post', 'user', 'type', 'created_at', 'updated_at']

# Notification serializer for user alerts.
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'text', 'read', 'created_at', 'updated_at']