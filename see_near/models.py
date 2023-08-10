# from datetime import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager


#슈퍼유저
class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("이메일을 입력해주세요!")
        if not password:
            raise ValueError("비밀번호를 입력해주세요!")

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# #사용자
# class User(AbstractBaseUser): 
#     user_id=models.CharField(max_length=200, default="쥬미")
#     password=models.CharField(max_length=200)
#     nickname=models.CharField(max_length=200)
#     user_name=models.CharField(max_length=200)
#     email=models.EmailField(max_length=200)
#     # address_location_1=models.CharField(max_length=200)
#     # address_location_2=models.CharField(max_length=200)
#     # address=models.CharField(max_length=200)
#     user_number=models.CharField(max_length=200)
#     # reg_date=models.DateTimeField(auto_now_add=True) 사용자 계정 만든 시간 굳이 저장할 필요없음
    
#     objects = UserManager()
    
#     def __str__(self):
#         return f'{self.nickname}(email: {self.email} id: {self.user_id})'
    
# # timezone.localtime()


#게시물
class Post(models.Model):
    #user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    post_id=models.AutoField(primary_key=True) #게시물 아이디
    title=models.CharField(max_length=200) #제목
    # create_time=models.DateTimeField(auto_now_add = True) #업데이트 시간
    # create_date = models.DateTimeField(auto_now_add=True)
    # update_date = models.DateTimeField(auto_now=True)
    content=models.TextField() #내용
    price=models.IntegerField() #가격
    situation=models.CharField(max_length=200, default="판매중") #거래 상황
    categories=models.CharField(max_length=100, default=None ) #카테고리
    images=models.ImageField(blank=True, upload_to="images/", null=True) #업로드된 이미지파일을 이미지에 저장
    
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:100]


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
    
#  #댓글   
# class Comment(models.Model):
#     userkey=models.ForeignKey('User', on_delete=models.CASCADE, db_column='userkey') #유저 넘버 참조
#     product_number=models.ForeignKey('Product', on_delete=models.CASCADE, db_column='product_number') #상품번호 참조
#     title=models.CharField(max_length=30)
#     content=models.TextField()

