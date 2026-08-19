from django.contrib import admin
from .models import Tag, Category, Post, Comment, Profile, Reaction

"""
Register the models to the Django admin site.
to test it. run the server and go to the admin page
"""
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Reaction)
# Register your models here.
