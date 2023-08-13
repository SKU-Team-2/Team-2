from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm
from .models import Category, Post, Cart, CartItem, seenear_user
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import PostSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from django.conf import settings


# 메인 화면(상품 정보를 전달하는 함수)
def product_list(request):
    products = Post.objects.all()
    sort_by = request.GET.get('sort', 'name')
    category_id = request.GET.get('category')

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        products = Post.objects.filter(categories=category)
    else:
        products = Post.objects.all()
    
    if sort_by == 'name':
        products = Post.objects.order_by('title')
    elif sort_by == 'date':
        products = products.order_by('-pub_date')
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

# 상품 상세정보
def product_detail(request, post_id):
    post=get_object_or_404(Post, post_id=post_id)
    
    return render(
        request,
        'see_near/post_detail.html',
        {
            'post':post,
        }
    )
    
# 카테고리 분류 함수(왜안될까)
def post_list_by_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    posts = Post.objects.filter(categories=category)
    
    context = {
        'category':category,
        'posts':posts
    }
    return render(request, 'see_near/category.html', context)

# 카테고리별 검색


# 글 작성
@login_required
def create_post(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.seller = request.user
            post.save()

            return redirect('home')
    else:
        form = ProductForm()
        categories = Category.objects.all()

    context = {'form': form, 'categories':categories}
    return render(request, 'see_near/create_post.html', context)

# 게시글 수정
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    
    if request.user == post.seller:  # 로그인한 사용자와 게시물 작성자 비교
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES, instance=post)

            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = ProductForm(instance=post)
        return render(request, 'see_near/edit_post.html', {'form': form, 'post': post})
    else:
        return redirect('home')  # 권한이 없는 경우 홈 화면으로 리다이렉트

# 게시글 삭제
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.seller == request.user:
        if request.method == "POST":
            post.delete()
            return redirect('home')
    else:
        return HttpResponseForbidden("You do not have permission to delete this post.")
    
    context = {'post': post}
    return render(request, 'see_near/delete_post.html', context)


# 댓글 작성


# 댓글 수정


# 댓글 삭제


# 검색창
def search(request):
    if request.method =='POST':
        searched = request.POST['searched']
        products = Post.objects.filter(title__contains=searched)
        return render(request, 'see_near/search.html', {'searched':searched, 'products':products})
    else:
        return render(request, 'see_near/search.html')
    
    
#--------------------여기부턴 장바구니에요--------------------

# 카트 저장하는 함수
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

#--------------------여기부턴 유저관리

# 회원가입
def register_sn(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        new_user = seenear_user(user_name=user_name, email=email, nickname=nickname, user_id=user_id, password=password)
        new_user.save()
        messages.success(request, '회원가입이 완료되었습니다.')
        return redirect('login')
    
    return render(request, 'see_near/register.html')

# 로그인
def login_sn(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        user = seenear_user.objects.filter(user_id=user_id, password=password).first()
        # user = authenticate(username=user_id, password=password)
        if user is not None:
            print(user)
            login(request, user)
            return redirect('home')
        else:
            # print(user)
            message = '아이디 또는 비밀번호가 틀렸습니다.'
            return render(request, 'see_near/login.html', {'message': message})

    return render(request, 'see_near/login.html')

# 로그아웃

# 회원정보 확인


#-----------------------여기부턴 결제

# 결제
def payment(request):
    if request.method == 'POST':
        # 결제 정보 처리 로직 추가
        # 아임포트 API 호출, 결제 정보 생성 등
        
        # 결제 정보를 템플릿으로 전달하여 보여줌
        context = {
                # 결제 정보 및 폼 데이터 등을 context에 추가
        }
        return render(request, 'see_near/payment.html', context)
    
    return render(request, 'see_near/payment.html')


#-----------------------여기부턴 swagger api
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @swagger_auto_schema(request_body=PostSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(request_body=PostSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
