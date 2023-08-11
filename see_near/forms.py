from django import forms
from .models import Post, Comment, Image

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'name', 'content', 'price', 'category', 'location']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']