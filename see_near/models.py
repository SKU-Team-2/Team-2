from datetime import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey

import uuid

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)  # Set is_superuser to True

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(username, password, **extra_fields)




# class SeenearUserManager(BaseUserManager):
#     def create_user(self, username, password, **extra_fields):
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

class seenear_user(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        permissions = [
            ("view_post", "Can view posts"),
            ("change_post", "Can change posts"),
            ("view_user", "Can view users"),
        ]

    username = models.CharField(max_length=200, unique=True)    
    password=models.TextField(max_length=200)
    nick_name=models.TextField(max_length=200)
    full_name=models.TextField(max_length=200)
    email=models.EmailField(max_length=254)
    address=models.TextField(max_length=200)
    user_number=models.TextField(max_length=200)
    reg_date=models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
# class SeenearUserManager(BaseUserManager):
#     def create_user(self, user_id, email, nickname, full_name, password, staff=False, admin=False, active=True):
#         # if not user_id:
#         #     raise ValueError('id를 입력해주세요!')
#         # if not password:
#         #     raise ValueError('비밀번호를 입력해주세요!')

#         user = self.model(email=self.normalize_email(email))
#         user.set_password(password)
#         user.user_id = user_id
#         user.nickname = nickname
#         user.full_name = full_name
#         user.staff = staff
#         user.admin = admin
#         user.active = active
#         user.save(using=self._db)
        
#         return user

#     def create_superuser(self, user_id, email, nickname, full_name, password):
#         user = self.create_user(
#             user_id,
#             email,
#             nickname,
#             full_name,
#             password,
#             staff = True,
#             admin = True
#         )
        
#         return user


# class seenear_user(AbstractBaseUser):  
#     user_id = models.CharField(max_length=200, unique=True)     # id
#     nickname = models.CharField(max_length=255, blank=True)     # nickname
#     email = models.EmailField(max_length=255, null=True)   # email
#     full_name = models.CharField(max_length=100)                # 이름
#     address = models.TextField(max_length=200, null=True)       # 주소

#     active = models.BooleanField(default=True)
#     staff = models.BooleanField(default=False)
#     admin = models.BooleanField(default=False)

#     USERNAME_FIELD = 'user_id'
#     REQUIRED_FIELDS = ['nickname', 'full_name', 'email']
#     objects = SeenearUserManager()
    
#     def __str__(self):
#         return self.user_id

#     def has_perm(self, perm, obj=None):
#         return self.admin

#     def has_module_perms(self, app_label):
#         return self.admin

#     @property
#     def is_staff(self):
#         return self.staff

#     @property
#     def is_superuser(self):
#         return self.admin
    
    
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
    seller = models.ForeignKey(seenear_user, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(blank=True, upload_to="images/", null=True) #업로드된 이미지파일을 이미지에 저장
    
    def __str__(self):
        return self.title
    
    # def summary(self):
    #     return self.content[:100]

# 댓글
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(seenear_user, on_delete=models.CASCADE)
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