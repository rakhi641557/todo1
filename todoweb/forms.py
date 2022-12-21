from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from API.models import Todos

class UserRegisterationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]
        #styling model form
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            }
        
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

       
class TodoForm(forms.ModelForm):

    class Meta:
        model=Todos
        fields=["task_name"]
        
        widgets={
            "task_name":forms.TextInput(attrs={"class":"form-control"})
        }