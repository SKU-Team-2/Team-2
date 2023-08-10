from django.urls import path
from . import views

app_name='cart'

urlpatterns = [#name 속성 추가

    path('index/', views.product_list, name = 'home'),
    path('index/post_write/', views.post_create, name = 'post_write'),
    path('index/post_write/post_detail/<int:post_id>', views.product_detail, name = 'post_detail'),
    path('index/post_write/post_detail/cart/<int:post_id>', views.add_cart, name = 'add_cart'),
]