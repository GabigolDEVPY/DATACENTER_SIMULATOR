from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from user.services.inventory_services import InventoryService

from server.models import Rack


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        racks = (
            Rack.objects.filter(user=self.request.user, is_selected=True)
            .prefetch_related("bays")
            .order_by("id")
        )

        context = super().get_context_data(**kwargs)
        context["data"] = {
            "racks": [{"id": rack.id, "position": rack.position, "name": rack.name,"bays": [{"id": bay.id, "status": bay.is_active, "position": bay.position} for bay in rack.bays.all()],}for rack in racks],
            "inventory_summary": InventoryService(self.request.user.id).get_inventory_summary(),
        }

        return context