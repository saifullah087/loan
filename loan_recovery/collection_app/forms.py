from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Students,Blog

class UserRegiterForm(UserCreationForm):
    email=forms.EmailField()
   # first_name =forms.TimeField()

    class Meta:
        model=User
        fields =['username','email','password1','password2']

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class Students(forms.Form):
    student_number = forms.IntegerField()
    f_name = forms.CharField()
    l_name = forms.CharField()
    dob = forms.DateField()
    address = forms.CharField()
    county = forms.CharField()
    phone_number = forms.CharField()
    email = forms.CharField()
    gpa = forms.IntegerField()
    passwords = forms.CharField()

    class Meta:
        model=Students
        fields =['student_number','f_name','l_name','dob','address','country','phone_number','email','gpa','password']

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title']
