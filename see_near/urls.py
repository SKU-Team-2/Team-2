from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create_post/', views.create_post, name='create_post'),
    path('search/', views.search, name='search'),
    path('detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.post_list_by_category, name='post_list_by_category'),
    # path('cart/<int:post_id>/', views.add_cart, name='add_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)