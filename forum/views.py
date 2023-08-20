from django.shortcuts import render, get_object_or_404
from .models import Post


def forum_home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'forum/forum_home.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'forum/post_detail.html', context)
