from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AIModel
from django.shortcuts import get_object_or_404

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "models.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["models"] = AIModel.objects.filter(level=1)
        return context
    
class IAModelDetailView(View):
    def get(self, request, id):
        context = {
                "model": get_object_or_404(AIModel, id=id)
            }
        
        return render(request, template_name="partials/ia_modal.html", context=context)