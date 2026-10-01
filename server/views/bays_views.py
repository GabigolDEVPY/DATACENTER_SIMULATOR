from django.shortcuts import render
from django.views.generic import View
from server.services.bay_service import BayService
from server.services.BayContextService import BayContextService
from server.services.BayApplicationService import BayApplicationService




class ChangeStatusBay(View):
    def post(self, request, id):
        context = BayApplicationService.change_status(request.user.id, id)
        bay_service = BayService(bay_id=id)
        return render(request, template_name="partials/bay_status_response.html", context=context)
    
    
class GetBayDetail(View):
    def get(self, request, id):
        context = BayContextService.get_bay_context(request.user.id, id)
        return render(request, template_name="partials/modal_bay.html", context=context)
    
    
class ChangeComponent(View):
    def post(self, request, id):
        service = BayService(bay_id=id).change_component(request.POST.get("field"), request.POST.get("component_id"), request.user.id)
        context = BayContextService.get_bay_context(request.user.id, id)
        return render(request, template_name="partials/modal_bay.html", context=context)
    
class RemoveComponent(View):
    def post(self, request, id):
        service = BayService(bay_id=id).remove_component(request.POST.get("field"))
        context = BayContextService.get_bay_context(request.user.id, id)
        return render(request, template_name="partials/modal_bay.html", context=context)