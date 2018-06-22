from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
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
    paginate_by = 5


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


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 增加阅读量； self.object 的值就是被访问的文章实例 post
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 text 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.text = markdown.markdown(post.text,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comments.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


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
