from app.models import Post
from django.shortcuts import render


# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "app/index.html", context=context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    context = {"post": post}
    return render(request, "app/post.html", context=context)
