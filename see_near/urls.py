from django.urls import path
from . import views

urlpatterns = [#name 속성 추가

    path('index/', views.home, name = 'home'),
    path('index/post_write/', views.post_create, name = 'post_write'),
    path('index/post_write/post_detail/<int:post_id>', views.product_detail, name = 'post_detail'),
    # path('index/post', views.home, name = 'home'),
    # path('index/signin', views.)
]