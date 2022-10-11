from .models import Post
from django.forms import ModelForm

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'created', 'id', 'tags', 'likes', 'dislikes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
