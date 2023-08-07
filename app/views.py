from app.models import Post
from django.shortcuts import render


# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "app/index.html", context=context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()
    context = {"post": post}
    return render(request, "app/post.html", context=context)
