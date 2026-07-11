import sys
sys.dont_write_bytecode = True
from django.shortcuts import render
from django.views.generic import View
from ..models import Bay
from user.models import InventoryItem


class ChangeStatusBay(View):
    def post(self, request, id):
        bay = Bay.objects.filter(id=id).first()
        bay.is_active = not bay.is_active
        bay.save()
        return render(request, template_name="partials/bay.html", context={"bay": bay})
    
class GetBayDetail(View):
    def get(self, request, id):
        bay = Bay.objects.filter(id=id).first()
        context = {"bay": bay, 
                   "rams": InventoryItem.objects.filter(item__ram__isnull=False),
                   "cpus": InventoryItem.objects.filter(item__cpu__isnull=False),
                   "gpus": InventoryItem.objects.filter(item__gpu__isnull=False),
                   "ssds": InventoryItem.objects.filter(item__ssd__isnull=False),
                   }
        return render(request, template_name="partials/modal_bay.html", context=context)