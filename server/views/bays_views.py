import sys
sys.dont_write_bytecode = True
from django.shortcuts import render
from django.views.generic import View, TemplateView
from ..models import Rack, Bay


class ChangeStatusBay(View):
    def post(self, request, id):
        bay = Bay.objects.filter(id=id).first()
        bay.is_active = not bay.is_active
        bay.save()
        return render(request, template_name="partials/bay.html", context={"bay": bay})