from django.forms import ModelForm
from .models import Message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})