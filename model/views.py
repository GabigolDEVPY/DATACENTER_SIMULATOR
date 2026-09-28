from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from model.services.IaApplicationService import IaModelContextServices


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "models.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(IaModelContextServices.get_ia_models(self.request.user.id))
        return context


class IAModelDetailView(LoginRequiredMixin, View):
    template_name = "partials/ia_modal.html"

    def get(self, request, id):
        context = IaModelContextServices.get_ia_model(request.user.id, id)
        return render(request, self.template_name, context)


class IaModelRun(LoginRequiredMixin, View):
    def post(self, request, id):
        return JsonResponse({"status": "ok"})
    
class IaModelInstall(LoginRequiredMixin, View):
    def post(self, request):
        
        time = IaModelContextServices.install_ia_model(request.user.id, request.POST)
        context = IaModelContextServices.get_ia_model(request.user.id, request.POST.get("ia_model_id"))
        context["time"] = time
        
        return render(request, "partials/ia_modal.html", context=context)