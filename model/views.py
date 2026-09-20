from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from model.services.ia_model_context_service import IaModelContextServices
from django.http import JsonResponse

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "models.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = IaModelContextServices.get_ia_models(self.request.user.id)
        return context
    
    
    
class IAModelDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        context = IaModelContextServices.get_ia_model(self.request.user.id, id)
        return render(request, template_name="partials/ia_modal.html", context=context)
    
class IaModelRun(LoginRequiredMixin, View):
    def post(self, request, id):
        print(request.POST)
        return JsonResponse({
            "fdsfd": 200
        })
        
        