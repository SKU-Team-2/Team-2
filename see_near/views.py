from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm

from .models import Category, Post, Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


#메인 화면(상품 정보를 전달하는 함수)
def product_list(request):
    products = Post.objects.all()
    sort_by = request.GET.get('sort', 'name')
    category_id = request.GET.get('category')

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        products = Post.objects.filter(p_category=category)
    else:
        products = Post.objects.all()
    
    if sort_by == 'name':
        products = Post.objects.order_by('title')
    searched = request.GET.get('searched', '')
    if searched:
        products = products.filter(title__icontains=searched)
    
    categories = Category.objects.all()
    
    context = {
        'products':products,
        'categories':categories,
        'searched':searched
    }
    
    return render(request, 'see_near/home.html', context)



def product_detail(request, post_id):
    post=get_object_or_404(Post, post_id=post_id)
    
    return render(
        request,
        'see_near/post_detail.html',
        {
            'post':post,
        }
    )
    
# 카테고리 분류 함수
def post_list_by_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    posts = Post.objects.filter(p_category=category)
    
    context = {
        'category':category,
        'posts':posts
    }
    return render(request, 'see_near/category.html', context)

    
#상품 글을 작성해 html로 보내는 함수
def create_post(request):
    post = Post.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            post.save()

        return product_list(request)

    else:
        form = ProductForm()
        categories = Category.objects.all()

    context = {'form': form, 'categories':categories}
    return render(request, 'see_near/create_post.html', context)

#검색창
def search(request):
    if request.method =='POST':
        searched = request.POST['searched']
        products = Post.objects.filter(title__contains=searched)
        return render(request, 'see_near/search.html', {'searched':searched, 'products':products})
    else:
        return render(request, 'see_near/search.html')
    
    
#--------------------여기부턴 장바구니에요--------------------

#카트 저장하는 함수
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