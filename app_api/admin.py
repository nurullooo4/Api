from django.contrib import admin
from django.contrib.auth import get_user_model

from app_api.models import Post, Comment

User = get_user_model()

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)

