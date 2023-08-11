from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Post, Comment, Cart, CartItem
from see_near.forms import PostForm, ImageForm
from django.core.exceptions import ObjectDoesNotExist
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
    
def cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request, post_id): #카트에 저장 후 카트 페이지로 넘어감(이 아이로 넘겨줘야 함)
    product=Post.objects.get(pk=post_id)
    try:
        cart=Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=cart_id(request))
        cart.save()
        
    try:
        cart_item=CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
        
    return redirect('cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None): #카트 페이지 정보
    try:
        cart=Cart.objects.get(cart_id=cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    
    return render(request, 'see_near/cart.html', dict(cart_items=cart_items, total=total, counter=counter))