from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from model.services.ia_model_context_service import IaModelContextService
from model.services.ia_model_service import IaModelService


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "models.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(IaModelContextService.get_ia_models(self.request.user.id))
        return context


class IAModelDetailView(LoginRequiredMixin, View):
    template_name = "partials/ia_modal.html"

    def get(self, request, id):
        context = IaModelContextService.get_model_context(request.user.id, id)
        return render(request, self.template_name, context)


class IaModelRun(LoginRequiredMixin, View):
    def post(self, request, id):
        return JsonResponse({"status": "ok"})
    
    
class IaModelInstall(LoginRequiredMixin, View):
    def post(self, request):
        ia_model_id = request.POST.get("ia_model_id")
        bay_id = request.POST.get("bay_id")

        time = IaModelService.install_ia_model(
            user_id=request.user.id,
            model_id=ia_model_id,
            bay_id=bay_id,
        )
        context = IaModelContextService.get_model_context(request.user.id, ia_model_id)
        context["time"] = time
        
        return render(request, "partials/ia_modal.html", context=context)