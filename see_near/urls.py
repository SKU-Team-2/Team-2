from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [#name 속성 추가
    # 게시물
    path('', views.product_list, name = 'home'),
    path('create_post/', views.create_post, name = 'create_post'),
    path('post_detail/<int:post_id>/', views.product_detail, name='post_detail'),
    path('main/edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('main/delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.post_list_by_category, name='category'),
    # 장바구니
    path('post_detail/cart/<int:post_id>/', views.add_cart, name='add_cart'),
    path('post_detail/cart/', views.cart_detail, name='cart_detail'), 
    # 회원가입/로그인
    path('register_sn/', views.register_sn, name='register'),
    path('login_sn/', views.login_sn, name='login'),
    # 결제
    path('payment/', views.payment, name='payment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)