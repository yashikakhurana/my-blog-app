from app.forms import CommentForm, SubscribeForm
from app.models import Comment, Post
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by("-view_count")[0:3]
    recent_posts = Post.objects.all().order_by("-last_updated")[0:3]
    subscribe_form = SubscribeForm()
    subscribe_successful = None
    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_successful = "Subscribed successfully"

    context = {
        "posts": posts,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
        "subscribe_form": subscribe_form,
        "subscribe_successful": subscribe_successful,
    }
    return render(request, "app/index.html", context=context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    form = CommentForm()
    comments = Comment.objects.filter(post=post, parent=None)

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            parent_obj = None
            if request.POST.get("comment_parent"):
                # save reply considering comment parent
                comment_parent = request.POST.get("comment_parent")
                parent_obj = Comment.objects.get(id=comment_parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(
                        reverse("post_page", kwargs={"slug": slug})
                    )

            else:
                # comment only
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
