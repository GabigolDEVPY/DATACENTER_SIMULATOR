import sys
sys.dont_write_bytecode = True
from django.shortcuts import render
from django.views.generic import View, TemplateView
from hardware.models import RAM, CPU, GPU, SSD
from ..models import Rack, Bay

class HomeView(TemplateView):
    template_name = 'datacenter/index.html'     
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hacks"] = Rack.objects.all()
        return context


class GetBayDetail(View):
    def get(self, request, id):
        bay = Bay.objects.filter(id=id).first()
        context = {"bay": bay, "rams": RAM.objects.all(), "cpus": CPU.objects.all(), "gpus": GPU.objects.all(), "ssds": SSD.objects.all()}
        print("Bay Detail Context:", context)  # Debugging line to check the context
        return render(request, template_name="partials/modal_bay.html", context=context)
