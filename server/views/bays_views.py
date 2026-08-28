from django.shortcuts import render
from django.views.generic import View
from server.services.bay_service import BayService
from user.services.inventory_services import InventoryService



class ChangeStatusBay(View):
    def post(self, request, id):
        bay = BayService(id).change_status()
        return render(request, template_name="partials/bay.html", context={"bay": bay})
    
    
class GetBayDetail(View):
    def get(self, request, id):
        bay = BayService(bay_id=id).get_view_model()
        inventory = InventoryService(request.user.id)
        context = {
            "bay": bay,
            "cpus": inventory.get_cpus(),
            "gpus": inventory.get_gpus(),
            "rams": inventory.get_rams(),
            "ssds": inventory.get_ssds()
        }
        return render(request, template_name="partials/modal_bay.html", context=context)
    
class ChangeComponent(View):
    def post(self, request, id, component_id):
        pass