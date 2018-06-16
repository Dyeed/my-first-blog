from django.db import models
from django.utils import timezone


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
