from django.shortcuts import render
from django.views.generic import View
from server.services.bay_service import BayService
from server.services.BayApplicationService import BayApplicationService



class ChangeStatusBay(View):
    def post(self, request, id):
        context = BayApplicationService.change_status(request.user.id, id)
        return render(request, template_name="partials/bay_status_response.html", context=context)
    
    
class GetBayDetail(View):
    def get(self, request, id):
        context = BayApplicationService.get_bay_model_context(request.user.id, bay_id=id)
        return render(request, template_name="partials/modal_bay.html", context=context)
    
    
class ChangeComponent(View):
    def post(self, request, id):
        context = BayApplicationService.change_component(request.POST, request.user.id, id)
        return render(request, template_name="partials/modal_bay.html", context=context)
    
class RemoveComponent(View):
    def post(self, request, id):
        context = BayApplicationService.remove_component(request.POST, request.user.id, id)
        return render(request, template_name="partials/modal_bay.html", context=context)