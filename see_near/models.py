# from datetime import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey

import uuid

class SeenearUserManager(BaseUserManager):
    def create_user(self, user_id=None, password=None, **extra_fields):
        if user_id is None:
            user_id = str(uuid.uuid4())

        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id=None, password=None, **extra_fields):
        if user_id is None:
            user_id = str(uuid.uuid4())
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if password is None:
            raise ValueError("The 'password' argument must be provided when creating a superuser.")

        return self.create_user(user_id=user_id, password=password, **extra_fields)


class seenear_user(AbstractBaseUser):
    user_number = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=200, unique=True)    
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)   # 이름
    nick_name = models.CharField(max_length=200)               # 닉네임
    email = models.EmailField(max_length=254)                  # 이메일
    address = models.TextField(max_length=200)                 # 주소
    reg_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    objects = SeenearUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.nick_name
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
# 카테고리
class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

# 게시물
class Post(models.Model):
    post_id = models.AutoField(primary_key=True) #게시물 아이디
    title = models.CharField(max_length=100) # 제목
    name = models.CharField(max_length=100)  # 제품명
    content = models.TextField() #내용
    price = models.IntegerField() #가격
    situation = models.CharField(max_length=200, default="판매중") #거래 상황
    categories = models.ManyToManyField(Category)
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(blank=True, upload_to="images/", null=True) #업로드된 이미지파일을 이미지에 저장
    
    def __str__(self):
        return self.title
    
    # def summary(self):
    #     return self.content[:100]

# 댓글
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    C_pub_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author.username}의 댓글"

# 장바구니 모델
class Cart(models.Model):
    cart_id=models.CharField(max_length=250, blank=True)
    date_added=models.DateField(auto_now_add=True)
    class Meta:
        db_table='Cart'
        ordering=['date_added']
        
    def __str__(self):
        return self.cart_id

    
class CartItem(models.Model):
    product=models.ForeignKey(Post, on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    active=models.BooleanField(default=True)
    class Meta:
        db_table='CarItem'
        
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product