from app.models import Post
from django.shortcuts import render

# Create your views here.


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    context = {"post": post}
    return request(request, "app/post.html", context=context)
