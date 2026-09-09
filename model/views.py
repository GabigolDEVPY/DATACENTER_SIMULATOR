from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from model.services.ia_model_context_service import IaModelContextServices

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "models.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ia_models, ia_models = IaModelContextServices.get_ia_models(self.request.user.id)
        context["ia_models"] = ia_models
        context["user_ia_models"] = user_ia_models
        return context
    
class IAModelDetailView(View):
    def get(self, request, id):
        ia_model = IaModelContextServices.get_ia_model(self.request.user.id, id)
        context = {
                "model": ia_model
            }
        
        return render(request, template_name="partials/ia_modal.html", context=context)