# from datetime import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

# #슈퍼유저
# class UserManager(BaseUserManager):
#     def create_user(self, email, password):
#         if not email:
#             raise ValueError("이메일을 입력해주세요!")
#         if not password:
#             raise ValueError("비밀번호를 입력해주세요!")

#         email = self.normalize_email(email)
#         user = self.model(email=email)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user

#     def create_superuser(self, email, password):
#         user = self.create_user(email, password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)

#         return user

class SeenearUserManager(BaseUserManager):
    def create_user(self, user_id, password, **extra_fields):
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class seenear_user(AbstractBaseUser):
    user_id=models.TextField(max_length=200)
    password=models.TextField(max_length=200)
    nickname=models.TextField(max_length=200)
    user_name=models.TextField(max_length=200)
    email=models.EmailField(max_length=254)
    address=models.TextField(max_length=200)
    user_number=models.TextField(max_length=200)
    reg_date=models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    objects = SeenearUserManager()

    USERNAME_FIELD = 'user_id'

    def __str__(self):
        return self.user_id
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

#카테고리(글이 있으면 삭제가 안됨 ㅠ)
class Category(models.Model):
    name = models.CharField(max_length=100)
    # category_id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return self.name

#게시물
class Post(models.Model):
    post_id = models.AutoField(primary_key=True) #게시물 아이디
    title = models.CharField(max_length=100) # 제목
    name = models.CharField(max_length=100)  # 제품명
    content = models.TextField() #내용
    price = models.IntegerField() #가격
    situation = models.CharField(max_length=200, default="판매중") #거래 상황
    categories = models.ForeignKey(Category, on_delete=models.CASCADE) #카테고리
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    images = models.ImageField(blank=True, upload_to="images/", null=True) #업로드된 이미지파일을 이미지에 저장
    
    def __str__(self):
        return self.title
    
    # def summary(self):
    #     return self.content[:100]

# 댓글
class Comment(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    C_pub_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author.username}의 댓글"

#장바구니 모델
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