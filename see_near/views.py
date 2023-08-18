from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm
from .models import Category, Post, Cart, CartItem, seenear_user, Comment
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator

from rest_framework import viewsets
from .serializers import (
    CategorySerializer, PostSerializer, CommentSerializer,
    CartSerializer, CartItemSerializer, SeenearUserSerializer
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from django.conf import settings


# 메인 화면(상품 정보를 전달하는 함수)
def product_list(request):
    products = Post.objects.all()
    sort_by = request.GET.get('sort', 'name')
    category_id = request.GET.get('category')
    
    if request.method == "POST":
        if request.POST.get('category'):
            category_get = get_object_or_404(Category, id=request.POST.get('category'))
            
            return redirect('category', category_id=category_get.id)
        
    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        products = Post.objects.filter(categories=category)
    
    if sort_by == 'name':
        products = Post.objects.order_by('title')
    elif sort_by == 'date':
        products = products.order_by('-pub_date')
        
    searched = request.GET.get('searched', '')
    if searched:
        products = products.filter(title__icontains=searched)
        
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'products':products,
        'categories':categories,
        'searched':searched,
        'page_obj':page_obj
    }
    
    return render(request, 'see_near/Main.html', context)

# 상품 상세정보
def product_detail(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    comments = Comment.objects.filter(post=post)
    comment_count = comments.count()
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_instance = request.user
            content = request.POST.get('content', '').strip()

            if content:
                post_instance = Post.objects.get(pk=post.pk)
                comment = Comment(post=post_instance, nickname=user_instance, content=content)
                comment.save()
                return redirect('post_detail', post_id=post_id)
            
    return render(
        request,
        'see_near/post_detail.html', 
        {'post': post, 'comments': comments, 'comment_count': comment_count}
    )

# 카테고리 분류 함수
def category_view(request, category_id):
    selected_category = Category.objects.get(pk=category_id)
    category_posts = Post.objects.filter(categories=selected_category)
    
    paginator = Paginator(category_posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'selected_category_id': selected_category,
        'category_posts': category_posts,
        'page_obj':page_obj
    }

    return render(request, 'see_near/category.html', context)

# 게시물 생성
@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST['title']
        name = request.POST['name']
        content = request.POST['content']
        price = request.POST['price']
        situation = request.POST.get('situation', "판매중")  # 기본값 설정
        category_id = request.POST['category']
        images = request.FILES['image'] if 'image' in request.FILES else None
        
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            pass
        
        post = Post(
            title=title,
            name=name,
            content=content,
            price=price,
            situation=situation,
            categories=category,
            seller=request.user,
            images=images
        )
        post.save()

        return redirect('home')
    else:
        categories = Category.objects.all()

    return render(request, 'see_near/create_post.html', {'categories': categories})


# 게시글 수정
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    print(post.seller)
    
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
    print(post.seller)
    
    if post.seller == request.user:
        if request.method == "POST":
            post.delete()
            return redirect('home')
    else:
        return HttpResponseForbidden("You do not have permission to delete this post.")
    
    context = {'post': post}
    return render(request, 'see_near/delete_post.html', context)

# 댓글 수정
@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.method == 'POST':
        comment.content = request.POST.get('content', '').strip()
        comment.save()
        return redirect('post_detail', post_id=comment.post.pk)
        
    return render(request, 'see_near/comment_edit.html', {'comment': comment})


# 댓글 삭제
@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.method == 'POST':
        post_pk = comment.post.pk  # Store the post pk before deleting the comment
        comment.delete()
        return redirect('post_detail', post_id=post_pk)  # Redirect to the correct post detail page
    
    return render(request, 'see_near/comment_delete.html', {'comment': comment})


# 검색창
def search(request):
    if request.method =='POST':
        searched = request.POST['searched']
        products = Post.objects.filter(title__contains=searched)
        
        paginator = Paginator(products, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'see_near/search.html', {'searched':searched, 'products':products, 'page_obj':page_obj})
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

def minus_cart(request, post_id):
    product=Post.objects.get(pk=post_id)
    
    try:
        cart=Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=cart_id(request))
        cart.save()
        
    try:
        cart_item=CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity >= 2:
            cart_item.quantity -= 1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
        
    return redirect('cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None, selected=None): #카트 페이지 정보
    try:
        selected = request.POST.getlist('selected')
        cart=Cart.objects.get(cart_id=cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    
    return render(request, 'see_near/cart.html', dict(cart_items=cart_items, total=total, counter=counter, selected=selected))

def remove_selected(request):
    if request.method =="POST":
        selected_items=request.POST.getlist('selected')
        cart=Cart.objects.get(cart_id=cart_id(request))
        
        for item_id in selected_items:
            cart_item=get_object_or_404(CartItem, id=item_id)
            if cart_item.cart ==cart:
                cart_item.delete()
                
    return redirect('cart_detail')

#--------------------여기부턴 유저관리

# 회원가입
def register(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        address = request.POST.get('address')
        Inputname = request.POST.get('Inputname')
        
        # 아이디 중복 확인
        if seenear_user.objects.filter(user_id=user_id).exists():
            message = '이미 사용 중인 아이디입니다.'
            return render(request, 'see_near/register.html', {'message': message})

        # 닉네임 중복 확인
        if seenear_user.objects.filter(nickname=nickname).exists():
            error_message = '이미 사용 중인 닉네임입니다.'
            return render(request, 'see_near/register.html', {'error_message': error_message})

        new_user = seenear_user.objects.create_user(user_id=user_id, email=email, nickname=nickname, full_name=full_name, password=password, address=address, Inputname=Inputname)
        print(new_user)
        new_user.save()
        
        messages.success(request, '회원가입이 완료되었습니다.')
        return redirect('login')
    
    return render(request, 'see_near/register.html')

# 로그인
def login_sn(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        user = authenticate(username=user_id, password=password)
        if user is not None:
            print(user)
            login(request, user)
            return redirect('home')
        else:
            print(user, '...')
            message = '아이디 또는 비밀번호가 틀렸습니다.'
            return render(request, 'see_near/login.html', {'message': message})

    return render(request, 'see_near/login.html')

# 로그아웃
@login_required
def logout_view(request):
    logout(request)
    return redirect("home")

# 마이페이지
@login_required
def user_page(request, pk):
    user = get_object_or_404(seenear_user, pk=pk)
    if request.method == 'POST':
        user.full_name = request.POST['full_name']
        user.email = request.POST['email']
        user.nickname = request.POST['nickname'] 
        user.user_id = request.POST['user_id'] 
        user.password = request.POST.get('password')  
        user.address = request.POST.get('address')
        user.Inputname = request.POST.get('Inputname')
        user.save()
        return redirect('home')
    return render(
      request,
      'see_near/mypage.html',
      {
         'user' : user,
      },
   )

# 회원정보 수정
@login_required
def update_user(request, pk):
    user = get_object_or_404(seenear_user, pk=pk)
    
    if request.method == 'POST':
        user.full_name = request.POST['full_name']
        user.email = request.POST['email']
        user.nickname = request.POST['nickname'] 
        user.user_id = request.POST['user_id'] 
        new_password = request.POST.get('password')
        user.address = request.POST.get('address')
        user.Inputname = request.POST.get('Inputname')
        if new_password:
            user.password = make_password(new_password)
        
        user.save()
        return redirect('home')
    
    return render(
        request,
        'see_near/user_update.html',
        {
            'user': user,
        },
    )
    
#-----------------------여기부턴 결제
# 결제
def payment(request):
    total = 0
    counter = 0
    cart_items = None
    
    if request.method == 'GET':
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
                
    context = {
        'cart_items': cart_items,
        'total': total,
        'counter': counter
    }
    
    return render(request, 'see_near/cart.html', context)


#-----------------------여기부턴 swagger api
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @swagger_auto_schema(request_body=PostSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(request_body=PostSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

class SeenearUserViewSet(viewsets.ModelViewSet):
    queryset = seenear_user.objects.all()
    serializer_class = SeenearUserSerializer
    permission_classes = [IsAuthenticated]