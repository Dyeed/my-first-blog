from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
import markdown


def post_list(request):
    """
    博客列表|首页
    :param request:
    :return:
    """
    # 根据发布时间逆序排列
    # **已在模型中处理
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/index.html', {'posts': posts, })


class IndexView(ListView):
    """首页
    CBV替代post_list()
    """
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'


def archives(request, year, month):
    """
    归档页
    :param request:
    :param year:
    :param month:
    :return:
    """
    posts = Post.objects.filter(created_date__year=year,
                                created_date__month=month,
                                ).order_by('-created_date')
    return render(request, 'blog/index.html', context={'posts': posts})


# 继承自IndexView
class ArchivesView(IndexView):
    """
    CBV替代category()
    """

    def get_queryset(self):
        year, month = self.kwargs.get('year'), self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_date__year=year, created_date__month=month, )


def category(request, pk):
    """
    分类页
    :param request:
    :param pk:
    :return:
    """
    cate = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=cate).order_by('-created_date')
    return render(request, 'blog/index.html', context={'posts': posts})


# 继承自IndexView
class CategoryView(IndexView):
    """
    CBV替代category()
    """

    def get_queryset(self):
        """
        类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性里，非命名组参数值保存在实例的 args 里
        :return:
        """
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


def post_detail(request, pk):
    """
    博客详情
    :param request:
    :param pk: (?P<pk>[0-9]+)
    :return:
    """
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.text = markdown.markdown(post.text,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comments.all()
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)


@login_required
def post_new(request):
    """
    新建博客页
    :param request:
    :return:
    """
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('index')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
            # return redirect('post_detail')
        else:
            comment_list = post.comments.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)
        # form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
