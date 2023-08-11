"""hackathon_sku_2team_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import see_near.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_post/', see_near.views.create_post, name='create_post'),
    path('search/', see_near.views.search, name='search'),
    path('', see_near.views.post_list, name='post_list'),
    path('post_detail/<int:post_id>/', see_near.views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', see_near.views.post_list_by_category, name='post_list_by_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)