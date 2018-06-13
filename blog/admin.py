from django.contrib import admin
from .models import Post, Comment, Tag, Category


class PostAdmin(admin.ModelAdmin):
    """
    Post表增加显示字段
    """
    list_display = ['title', 'created_date', 'published_date', 'category', 'author']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag)
