from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("server:home")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
        
# Create your views here.
class UserLoginView(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("server:home")
    redirect_authenticated_user = True
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("user:login")

        
    