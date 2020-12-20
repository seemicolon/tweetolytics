from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

# from .models import User

class Register(UserCreationForm):
    class Meta:

        model=User
        fields=('email','username','password1','password2')

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control my-2 p-4', 'placeholder': 'Enter Your Email'})
        self.fields['username'].widget.attrs.update({'class': 'form-control my-2 p-4', 'placeholder': 'Enter Your Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control my-2 p-4', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control my-2 p-4', 'placeholder': 'Confirm Password'})


