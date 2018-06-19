import markdown
from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags


class Category(models.Model):
    """
    文章分类
    name:类别
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        **admin后台会调用此方法，以显示名称而不是对象
        :return: 分类名
        """
        return self.name


class Tag(models.Model):
    """
    文章标签
    name：标签
    """
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    博文
    title：标题
    created_date：创建日期
    published_date：发布日期
    excerpt：文章摘要
    author：作者
    category:分类
    tags：标签
    text：文章正文
    """
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    excerpt = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField(to='Tag', blank=True)
    text = models.TextField()

    def published(self):
        """
        发布（时间）
        """
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        """
        审核评论
        """
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return '/post/{}/'.format(self.pk)

    def increase_views(self):
        """
        增加阅读量
        """
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            # 实例化 Markdown ，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            self.excerpt = strip_tags(md.convert(self.text))[:97]

        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    评论
    author：作者
    email：邮箱
    text：评论内容
    created_date：创建（提交）日期
    approved_comment：审核发布
    post：外键，关联博文表
    """
    author = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    text = models.TextField()
    # created_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')

    def approve(self):
        """
        审核评论
        :return:
        """
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
