from django import template
from ..models import Post, Category
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_date')[:num]


@register.simple_tag
def get_archives():
    """
    month精度、DESC降序排列
    :return:归档
    """
    return Post.objects.dates('created_date', 'month', order='DESC')


@register.simple_tag
def get_category():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    # return Category.objects.all()
