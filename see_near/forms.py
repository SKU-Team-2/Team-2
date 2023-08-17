from django import forms
from see_near.models import Post, Category, Comment


class ProductForm(forms.ModelForm): # ModelForm 은 장고 모델 폼
    class Meta: # 장고 모델 폼은 반드시 내부에 Meta 클래스 가져야 함
        model = Post
        fields = [ 'post_id', 'title' ,'name', 'price', 'content', 'categories', 'images','situation']
        labels = {
            'post_id': '게시물 번호',
            'title': '제품명 ',
            'price': '가격',
            'content': '내용',
            'categories': '카테고리',
            'images': '이미지',
            'situation': '거래상황'
        }
    title = forms.CharField(required=True)
    name = forms.CharField(required=True)
    price = forms.IntegerField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 4}))
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    images = forms.ImageField(required=True)  # 이미지 필드는 선택적으로 설정 가능
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']