from django.views import View
from django.shortcuts import render, get_object_or_404, redirect, reverse
from posts.models import Post
from posts.forms import PostForm
from django.contrib.auth import get_user_model

User = get_user_model()


def posts_list_view(request):

    if not request.user.is_authenticated:
        return redirect(reverse('login_url'))

    if request.method == 'GET':
        if request.user.role == User.UserType.ORDINARY:
            posts = request.user.posts.all()
        else:
            posts = Post.objects.all()

        return render(request, 'posts/index.html', context={'posts': posts})



def post_detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request,
                  'posts/post_detail.html',
                  {'post': post,}
)


class PostCreateView(View):

    form = PostForm
    template = 'posts/post_create.html'
    has_author = True


class PostUpdateView(View):

    bound_form = PostForm
    obj_class = Post
    template = 'posts/post_update.html'


class PostDeleteView(View):

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        return render(request, 'posts/post_delete.html', context={'post': post})

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return redirect(reverse('posts_list_url'))
