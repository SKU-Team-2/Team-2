from django import forms
from see_near.models import Post


class ProductForm(forms.ModelForm): # ModelForm 은 장고 모델 폼
    class Meta: # 장고 모델 폼은 반드시 내부에 Meta 클래스 가져야 함
        model = Post
        fields = [ 'post_id', 'title' ,'price', 'content', 'categories', 'images','situation']
        labels = {
            'post_id': '게시물 번호',
            'title': '제품명 ',
            'price': '가격',
            'content': '내용',
            'categories': '카테고리',
            'images': '이미지',
            'situation': '거래상황'
        }