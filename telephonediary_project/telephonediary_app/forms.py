from django.contrib.auth.forms import UserCreationForm
from .models import User, Contact
from django.forms import ModelForm

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')

class PhoneForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'number', 'state', 'city']