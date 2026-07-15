import time
import sys
sys.dont_write_bytecode = True
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from server.services.balance_service import BalanceService
from django.http import HttpResponse


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'datacenter/index.html'     
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hacks"] = self.request.user.racks.all()
        return context

class GetTotalBalance(View):
    def get(self, request):
        user = request.user
        value = 0
        racks = user.racks.all()
        for rack in racks:
            print("entrou", flush=True)
            print(rack)
            for bay in rack.bays.all():
                value += (bay.get_power() / 10000)
        print(value)
        
        return HttpResponse(f"R$ {value:.2f}")