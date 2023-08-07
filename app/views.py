from app.forms import CommentForm
from app.models import Comment, Post
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "app/index.html", context=context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    form = CommentForm()
    comments = Comment.objects.filter(post=post)

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            post_id = request.POST.get("post_id")
            post = Post.objects.get(id=post_id)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post_page", kwargs={"slug": slug}))

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()

    context = {"post": post, "form": form, "comments": comments}
    return render(request, "app/post.html", context=context)
