from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,CreateView,FormView,ListView,DetailView
from todoweb.forms import UserRegisterationForm,LoginForm,TodoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from API.models import Todos
from django.utils.decorators import method_decorator
from django.contrib import messages
# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"you must login first")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

from django.urls import reverse_lazy

class RegistrationView(CreateView):
    template_name="register.html"
    form_class=UserRegisterationForm
    model=User
    success_url=reverse_lazy("signin")



class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm


    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                messages.error(request,"invalid credentials")
                print("invalid")
                return redirect("signin")
#templateview

@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    template_name="index.html"
           

@method_decorator(signin_required,name="dispatch")
class TodoListView(ListView):
    template_name="todo-list.html"
    model=Todos
    context_object_name="todos"



    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

  

@method_decorator(signin_required,name="dispatch")
class TodoCreateView(CreateView):
    template_name="todo-add.html"
    form_class=TodoForm
    model=Todos
    success_url=reverse_lazy("todo-list")

    def form_valid(self,form):
        form.instance.user=self.request.user
        messages.success(self.request,"todo created")
        return super().form_valid(form)


@method_decorator(signin_required,name="dispatch")        
class TodoDetailView(DetailView):
    template_name="todo-detail.html"
    model=Todos
    context_object_name="todo"
    pk_url_kwarg="id"
   

@signin_required
def todo_delete_view(request,*args,**kw):
    id=kw.get("id")
    Todos.objects.get(id=id).delete()
    messages.success(request,"todo has been deleted")
    return redirect("todo-list")

@signin_required
def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("signin")
