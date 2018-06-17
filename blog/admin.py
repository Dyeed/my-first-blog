from django.contrib import admin
from .models import Post, Comment, Tag, Category


class PostAdmin(admin.ModelAdmin):
    """
    Post表增加显示字段
    下方注册
    """
    list_display = ['title', 'created_date', 'published_date', 'category', 'author']


class CommentAdmin(admin.ModelAdmin):
    """
    评论表增加显示字段
    """
    list_display = ['author', 'email', 'text', 'post', 'approved_comment']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Tag)
