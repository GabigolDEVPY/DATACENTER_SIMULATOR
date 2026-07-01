from django.shortcuts import render
from django.views.generic import View, TemplateView
from .models import DataCenterHack, Bay

class HomeView(TemplateView):
    template_name = 'datacenter/index.html'     
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hacks"] = DataCenterHack.objects.all()
        return context


class GetBayDetail(View):
    def get(self, request, id):
        bay = Bay.objects.filter(id=id).first()
        return render(request, template_name="partials/modal_bay.html", context={"bay": bay})
