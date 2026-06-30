from django.shortcuts import render
from django.views.generic import View, TemplateView
from .models import DataCenterHack

class HomeView(TemplateView):
    template_name = 'datacenter/index.html'     
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hacks"] = DataCenterHack.objects.all()
        return context


