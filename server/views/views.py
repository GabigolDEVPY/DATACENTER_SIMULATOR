import sys
sys.dont_write_bytecode = True
from django.shortcuts import render
from django.views.generic import TemplateView
from ..models import Rack
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'datacenter/index.html'     
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hacks"] = self.request.user.racks.all()
        return context

