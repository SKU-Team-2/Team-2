from django.contrib import admin
from .models import Post, CartItem

admin.site.register([Post, CartItem]) #Admin 페이지에서 띄울 카테고리
