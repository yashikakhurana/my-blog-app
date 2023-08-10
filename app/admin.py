from django.contrib import admin

from app.models import Post, Profile, Tag, Comment, Subscribe, WebsiteMeta

# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Subscribe)
admin.site.register(Profile)
admin.site.register(WebsiteMeta)
