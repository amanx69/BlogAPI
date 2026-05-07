from django.contrib import admin
from .models import Post ,Category,Comment,Like ,Bookmark

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Bookmark)