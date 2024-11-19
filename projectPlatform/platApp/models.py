from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

"""
Django Models for Blog Platform

This module defines the foundational structure of a Blog Platform through four distinct Django models: Tag, Category, Post, and Comment. Each model serves a specific purpose in organizing, categorizing, and managing the content and interactions within the blog. Here is a brief overview of each model:

- Tag: Utilized for tagging posts with specific, searchable keywords. Tags help in filtering posts based on common themes or subjects, enhancing the navigability and user experience of the blog.

- Category: Similar to tags but used for broader categorization of posts. Categories facilitate the organization of posts into general themes or topics, allowing users to easily find content within specific domains of interest.

- Post: The core model representing the blog posts themselves. Posts include essential attributes such as title, content, author (linked to Django's built-in User model), creation and update timestamps, and relationships to both tags and categories. This model is central to the blog's functionality, enabling the creation, display, and management of blog content.

- Comment: Designed to support user engagement through comments on posts. The Comment model includes fields for the comment's content, its author (also linked to the User model), and an optional parent comment to enable threaded conversations. This model enriches the blog by allowing readers to participate in discussions, share feedback, and interact with both the content and other readers.

Together, these models form the backbone of the Blog Platform, supporting its content creation, categorization, and community interaction features. The structure and relationships defined herein are designed to provide a comprehensive and user-friendly blogging experience.

Note: Each model extends a BaseModel, incorporating common fields like creation and update timestamps to ensure consistency and reduce redundancy across the models. Detailed comments and docstrings are provided for each class and field to enhance clarity and facilitate collaboration among team members.

"""
class React(models.Model):
    employee = models.CharField(max_length=30)
    department = models.CharField(max_length=200)


class BaseModel(models.Model):
    """
    A base model to define common fields across all models.

    Fields:
    - created_at (DateTimeField): Automatically set to the current date and time when the model instance is first created.
    - updated_at (DateTimeField): Automatically updated to the current date and time every time the model instance is saved.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True  # This model will not be used to create any database table.
        ordering = ['-created_at']  # Default ordering of instances by creation date in descending order.

class Tag(BaseModel):
    """
    Tag model for categorizing posts with specific keywords.

    Attributes:
    - name (CharField): A unique name for the tag.
    """
    name = models.CharField(max_length=30, unique=True, verbose_name=_("Name"))

    def __str__(self):
        """String representation of the Tag model."""
        return self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class Category(BaseModel):
    """
    Category model for organizing posts into broader topics.

    Attributes:
    - name (CharField): A unique name for the category.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Name"))

    def __str__(self):
        """String representation of the Category model."""
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

class Post(BaseModel):
    """
    Post model represents the blog post itself.

    Attributes:
    - title (CharField): The title of the blog post.
    - content (TextField): The body content of the blog post.
    - author (ForeignKey): A foreign key linking to the Django's User model representing the author of the post.
    - tags (ManyToManyField): A many-to-many relationship to the Tag model.
    - category (ForeignKey): A foreign key link to the Category model. It's nullable to allow posts without a specific category.
    """
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name=_("Author"))
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name=_("Tags"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name=_("Category"))
    search_vector = SearchVectorField(null=True) # Field for full-text search using PostgreSQL's full-text search feature.

    def __str__(self):
        """String representation of the Post model."""
        return self.title

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        indexes = [GinIndex(fields=['search_vector'])]  # Index for the search_vector field to optimize full-text search queries.

class Comment(BaseModel):
    """
    Comment model for user comments on blog posts.

    Attributes:
    - post (ForeignKey): A foreign key linking to the Post model. Represents the post that the comment is associated with.
    - author (ForeignKey): A foreign key linking to Django's User model representing the author of the comment.
    - content (TextField): The content of the comment.
    - parent (ForeignKey): An optional self-referential foreign key to enable threading. Allows a comment to be a reply to another comment.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Post"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Author"))
    content = models.TextField(verbose_name=_("Content"))
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name=_("Parent Comment"))

    def __str__(self):
        """String representation of the Comment model."""
        return _("Comment by %(author)s on %(post)s") % {'author': self.author.username, 'post': self.post.title}

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='img/', default='img/default.png')
    biography = models.CharField(max_length=500, default='')
    location = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.user.username
    
class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')

    def __str__(self):
        return f'{self.user_following.username} followed {self.user_followed.username}'

class Reaction(BaseModel):
    """
    Model to capture user reactions (likes/dislikes) on blog posts.

    Attributes:
        post (ForeignKey): Link to the Post model, indicating which post the reaction is for.
        user (ForeignKey): Link to the user model (AUTH_USER_MODEL setting), indicating who made the reaction.
        type (CharField): Specifies the type of reaction, e.g., like or dislike.
    """
    post = models.ForeignKey(Post, related_name='reactions', on_delete=models.CASCADE, verbose_name=_("Post"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"))
    type = models.CharField(max_length=10, choices=(('like', 'Like'), ('dislike', 'Dislike')), verbose_name=_("Type"))

    class Meta:
        verbose_name = _("Reaction")
        verbose_name_plural = _("Reactions")
        unique_together = ('post', 'user')  # Ensures a user can only react once per post.

    def __str__(self):
        """String representation showing user's reaction type on a post."""
        return f"{self.user.username}'s {self.type} on {self.post.title}"


class Notification(BaseModel):
    """
    Model for user notifications, triggered by various interactions such as new reactions or comments on their posts.

    Attributes:
        recipient (ForeignKey): Link to the user model (AUTH_USER_MODEL setting) who is the recipient of the notification.
        text (CharField): The text content of the notification.
        read (BooleanField): Status indicating whether the notification has been read.
    """
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE, verbose_name=_("Recipient"))
    text = models.CharField(max_length=255, verbose_name=_("Text"))
    read = models.BooleanField(default=False, verbose_name=_("Read"))

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        """String representation showing notification details for a user."""
        return f"Notification for {self.recipient.username}: {self.text}"