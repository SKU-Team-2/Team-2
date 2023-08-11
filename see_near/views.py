from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Post, Comment
from see_near.forms import PostForm, ImageForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        
        if post_form.is_valid() and image_form.is_valid():
            post = post_form.save(commit=False)
            post.seller = request.user
            post.save()
            
            image = image_form.save(commit=False)
            image.post = post
            image.save()
            
            return redirect('post_list')
    else:
        post_form = PostForm()
        image_form = ImageForm()
        categories = Category.objects.all()
    return render(request, 'see_near/create_post.html', {'post_form':post_form, 'image_form':image_form, 'categories':categories})
    

def post_list_by_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    posts = Post.objects.filter(p_category=category)
    
    context = {
        'category':category,
        'posts':posts
    }
    return render(request, 'see_near/post_list_by_category.html', context)


def post_list(request):
    posts = Post.objects.all()
    sort_by = request.GET.get('sort', 'name')
    category_id = request.GET.get('category')

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        posts = Post.objects.filter(p_category=category)
    else:
        posts = Post.objects.all()
    
    if sort_by == 'name':
        posts = Post.objects.order_by('title')
    searched = request.GET.get('searched', '')
    if searched:
        posts = posts.filter(title__icontains=searched)
    
    categories = Category.objects.all()
    
    context = {
        'posts':posts,
        'categories':categories,
        'searched':searched
    }
    return render(request, 'see_near/post_list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    images = post.images.all()
    
    context = {
        'post':post,
        'seller':post.seller,
        'images':images
    }
    return render(request, 'see_near/post_detail.html', context)

def search(request):
    if request.method =='POST':
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched)
        return render(request, 'see_near/search.html', {'searched':searched, 'posts':posts})
    else:
        return render(request, 'see_near/search.html')