from app.forms import CommentForm, SubscribeForm, UserRegistrationForm
from app.models import Comment, Post, Profile, Tag, WebsiteMeta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login


def all_liked_posts(request):
    all_liked_posts = Post.objects.filter(likes=request.user)
    context = {"all_liked_posts": all_liked_posts}
    return render(request, "app/all_liked_posts.html", context=context)


def all_posts(request):
    all_posts = Post.objects.all()
    context = {"all_posts": all_posts}
    return render(request, "app/all_posts.html", context=context)


def all_bookmarked_posts(request):
    all_bookmarked_posts = Post.objects.filter(bookmarks=request.user)
    context = {"all_bookmarked_posts": all_bookmarked_posts}
    return render(request, "app/all_bookmarked_posts.html", context=context)


def like_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse("post_page", args=[str(slug)]))


def bookmark_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse("post_page", args=[str(slug)]))


def register_user(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        print("inside form", request)
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # once regsiter, login user
            login(request, user)
            return redirect("/")

    context = {"form": form}
    return render(request, "registration/signup.html", context=context)


def about_page(request):
    website_info = None
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    context = {
        "website_info": website_info,
    }
    return render(request, "app/about.html", context=context)


def search_posts(request):
    search_query = ""
    if request.GET.get("q"):
        search_query = request.GET.get("q")
    posts = Post.objects.filter(title__icontains=search_query)
    context = {"posts": posts, "search_query": search_query}
    return render(request, "app/search.html", context=context)


# Create your views here.
def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by("-view_count")[0:3]
    recent_posts = Post.objects.all().order_by("-last_updated")[0:3]
    featured_blog = Post.objects.filter(is_featured=True)
    subscribe_form = SubscribeForm()
    subscribe_successful = None
    website_info = None
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if featured_blog:
        featured_blog = featured_blog[0]
    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            # store session
            request.session["subscribed"] = True
            subscribe_successful = "Subscribed successfully"
            # reset form
            subscribe_form = SubscribeForm()

    context = {
        "posts": posts,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
        "subscribe_form": subscribe_form,
        "subscribe_successful": subscribe_successful,
        "featured_blog": featured_blog,
        "website_info": website_info,
    }
    return render(request, "app/index.html", context=context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    form = CommentForm()
    comments = Comment.objects.filter(post=post, parent=None)

    # Bookmark logic
    bookmarked = False
    if post.bookmarks.filter(id=request.user.id).exists():
        bookmarked = True
    is_bookmarked = bookmarked

    # Likes logic
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    number_of_likes = post.number_of_likes()
    is_post_liked = liked

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

    # sidebar

    recent_posts = Post.objects.exclude(id=post.id).order_by("-last_updated")[0:3]
    tags = Tag.objects.all()
    related_posts = Post.objects.exclude(id=post.id).filter(author=post.author)[0:3]

    context = {
        "post": post,
        "form": form,
        "comments": comments,
        "is_bookmarked": is_bookmarked,
        "is_post_liked": is_post_liked,
        "number_of_likes": number_of_likes,
        "recent_posts": recent_posts,
        "tags": tags,
        "related_posts": related_posts,
    }
    return render(request, "app/post.html", context=context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by("-view_count")[0:3]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by("-last_updated")[0:3]
    tags = Tag.objects.all()

    context = {
        "tag": tag,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
        "tags": tags,
    }
    return render(request, "app/tag.html", context=context)


def author_page(request, slug):
    author_profile = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(author=author_profile.user).order_by("-view_count")[
        0:3
    ]
    recent_posts = Post.objects.filter(author=author_profile.user).order_by(
        "-last_updated"
    )[0:3]

    context = {
        "author_profile": author_profile,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
    }
    return render(request, "app/author.html", context=context)
