from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from user.services.inventory_services import InventoryService
from server.models import Rack

from django.forms.models import model_to_dict

def get_context_game(request):
    racks = Rack.objects.filter(user=request.user, is_selected=True).prefetch_related("bays").order_by("id")
    data = {
        "racks": [{"id": rack.id, "position": rack.position, "name": rack.name, "bays": [{"id": bay.id, "status": bay.is_active, "position": bay.position} for bay in rack.bays.all()]} for rack in racks],
        "inventory_summary": InventoryService(request.user.id).get_inventory_summary(),
        "datacenter": model_to_dict(request.user.datacenter.all().first()) if request.user.datacenter.exists() else None,
    }
    return data


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = get_context_game(self.request)

        return context