#from django.contrib.auth.forms
from django.forms import ModelForm
from .models import Profile, Instrument
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'friend', 'created', 'id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            # field.widget.attrs.update({'placeholder': name})

class InstrumentForm(ModelForm):
    class Meta:
        model = Instrument
        fields = ['name', 'level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if name == 'name':
                field.widget.attrs.update({'placeholder': 'Instrument'})
            else:
                field.widget.attrs.update({'placeholder': 'level'})

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if name == 'password1':
                field.widget.attrs.update({'placeholder': 'password'})
            elif name == 'password2':
                field.widget.attrs.update({'placeholder': 'confirm password'})
            else:
                field.widget.attrs.update({'placeholder': name})