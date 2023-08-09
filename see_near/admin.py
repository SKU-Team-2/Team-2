from django.contrib import admin
from .models import Post

admin.site.register([Post]) #Admin 페이지에서 띄울 카테고리
