import sys
sys.dont_write_bytecode = True
from django.shortcuts import render
from django.views.generic import TemplateView
from ..models import Rack

class HomeView(TemplateView):
    template_name = 'datacenter/index.html'     
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hacks"] = Rack.objects.all()
        return context

