from django.shortcuts import render
from django.views.generic import View
from ..models import Bay
from user.models import InventoryItem
from server.services.bay_services import BayService



class ChangeStatusBay(View):
    def post(self, request, id):
        bay = BayService(id)
        return render(request, template_name="partials/bay.html", context={"bay": bay})
    
    
class GetBayDetail(View):
    def get(self, request, id):
        context = BayService.get_bay_detail(id)
        return render(request, template_name="partials/modal_bay.html", context=context)