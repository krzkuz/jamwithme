#from django.contrib.auth.forms
from django.forms import ModelForm
from .models import Profile, Instrument


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'friend', 'created', 'id']

class InstrumentForm(ModelForm):
    class Meta:
        model = Instrument
        fields = ['name', 'level']