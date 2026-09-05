from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AIModel

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "models.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["models"] = AIModel.objects.all()
        return context
