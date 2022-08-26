from .models import Post
from django.forms import ModelForm

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'created', 'id', 'tags']