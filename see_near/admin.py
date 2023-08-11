from django.contrib import admin
from .models import Category, Post, Comment, Image, Cart, CartItem

# Register your models here.

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'parent_category')
#     list_filter = ('parent_category', )
#     search_fields = ('name', )
    
admin.site.register([Category, Post, Comment, Image, CartItem, Cart])