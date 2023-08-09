from django.shortcuts import redirect, render
from .forms import ProductForm

from .models import Post, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

#메인 화면
def home(request):
    product_list(request)
    return render(request, 'see_near/index.html')

#상품 정보를 전달하는 함수
def product_list(request):
    products = Post.objects.all()

    return render(
        request,
        'see_near/index.html', #메인 홈 화면
        {
            'products': products
        }
    )

def product_detail(request):
    products = Post.objects.all()
    
    return render(
        request,
        'see_near/post_detail.html',
        {
            'products':products
        }
    )
    
    
#상품 글을 작성해 html로 보내는 함수
def post_create(request):
    post = Post.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            #post.post_id = request.POST.get('post_id', '')
            # post.title = request.POST['title']
            # post.price = request.POST['price']
            # post.categories = request.POST['categories']
            # post.content = req uest.POST['content']
            # post.situation = request.POST['situation']
            # post.user = request.user

            post.save()

        return product_list(request)

    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'see_near/post_write.html', context)

#카트 저장하는 함수
def cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request, post_id): #카트에 저장 후 카트 페이지로 넘어감
    product=Post.objects.get(id=post_id)
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
    return redirect('cart:cart_detail')

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