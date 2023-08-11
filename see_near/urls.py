from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [#name 속성 추가

    path('index/', views.product_list, name = 'home'),
    path('index/create_post/', views.create_post, name = 'create_post'),
    path('index/search/', views.search, name='search'),
    path('index/post_write/post_detail/<int:post_id>/', views.product_detail, name='post_detail'),
    path('index/category/<int:category_id>/', views.post_list_by_category, name='category'), #카테고리
    #장바구니
    path('index/post_write/post_detail/cart/<int:post_id>/', views.add_cart, name='add_cart'),
    path('index/post_write/post_detail/cart/', views.cart_detail, name='cart_detail'), 

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)