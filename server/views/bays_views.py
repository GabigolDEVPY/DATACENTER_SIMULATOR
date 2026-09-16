from django.shortcuts import render
from django.views.generic import View
from server.services.bay_service import BayService
from server.services.bay_context_service import BayContextService



class ChangeStatusBay(View):
    def post(self, request, id):
        bay, components = BayContextService.change_status(request.user.id, id)
        context = {"bay": bay, **components}
        return render(request, template_name="partials/bay_status_response.html", context=context)
    
    
class GetBayDetail(View):
    def get(self, request, id):
        bay, components = BayContextService.get_bay_model_context(request.user.id, bay_id=id)
        context = {"bay": bay, **components}
        return render(request, template_name="partials/modal_bay.html", context=context)
    
    
class ChangeComponent(View):
    def post(self, request, id):
        bay, components = BayContextService.change_component(request.POST, request.user.id, id)
        context = {"bay": bay, **components}
        return render(request, template_name="partials/modal_bay.html", context=context)
    
class RemoveComponent(View):
    def post(self, request, id):
        bay, components = BayContextService.remove_component(request.POST, request.user.id, id)
        context = {"bay": bay, **components}
        return render(request, template_name="partials/modal_bay.html", context=context)