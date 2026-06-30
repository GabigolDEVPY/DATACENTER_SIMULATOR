from django.shortcuts import render
from django.views.generic import View
from .models import DataCenterHack

class HomeView(View):
    def get(self, request):
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["hacks"] = DataCenterHack.objects.all()
            return context
    
    
        return render(request, 'datacenter/index.html')
