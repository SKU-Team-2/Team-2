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

#게시물
class Post(models.Model):
    post_id=models.AutoField(primary_key=True) #게시물 아이디
    title=models.CharField(max_length=200) #제목
    content=models.TextField() #내용
    price=models.IntegerField() #가격
    situation=models.CharField(max_length=200, default="판매중") #거래 상황
    categories=models.CharField(max_length=100, default=None ) #카테고리
    images=models.ImageField(blank=True, upload_to="images/", null=True) #업로드된 이미지파일을 이미지에 저장
    
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:100]
    
    def get_comments(self):
        # Comment 객체 호출
        return self.comments.all()


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
    

