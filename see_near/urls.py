from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

from rest_framework import routers

router = routers.DefaultRouter() # DefaultRouter를 설정
router.register(r'Post', views.PostViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'carts', views.CartViewSet)
router.register(r'cart-items', views.CartItemViewSet)
router.register(r'users', views.SeenearUserViewSet)


urlpatterns = [
    # 게시물
    path('', views.product_list, name = 'home'),
    path('create_post/', views.create_post, name = 'create_post'),
    path('post_detail/<int:post_id>/', views.product_detail, name='post_detail'),
    path('main/edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('main/delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    # 댓글
    path('coment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    # 장바구니
    path('post_detail/add_cart/<int:post_id>/', views.add_cart, name='add_cart'),
    path('post_detail/minus_cart/<int:post_id>/', views.minus_cart, name='minus_cart'),
    path('post_detail/remove_selected/', views.remove_selected, name='remove_selected'),
    path('post_detail/cart/', views.cart_detail, name='cart_detail'), 
    # 결제
    path('cart/payment/', views.payment, name='payment'),
    # 회원가입/로그인
    path('register/', views.register, name='register'),
    path('login/', views.login_sn, name='login'),
    path("logout/", views.logout_view, name='logout'),
    path('user_page/<int:pk>/', views.user_page, name='user_page'),
    path('update_user/<int:pk>/', views.update_user, name='update_user'),
    # swagger api
    path('', include(router.urls))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)