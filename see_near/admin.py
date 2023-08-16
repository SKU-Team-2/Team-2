from django.contrib import admin
from .models import Post, CartItem, Category, Comment, seenear_user
from django.contrib.auth.admin import UserAdmin

admin.site.register(Post) #Admin 페이지에서 띄울 카테고리
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(seenear_user)