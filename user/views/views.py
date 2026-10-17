from django.views.generic import View
from ..services.services import UserService
from ..services.inventory_services import InventoryService
from django.http import JsonResponse



        
class GetBalanceView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            UserService.refresh_balance(user)
            return JsonResponse({"balance": str(user.money)})
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)

class GetInventoryView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            inventory_summary = InventoryService(user).get_inventory_summary()
            return JsonResponse({"inventory_summary": inventory_summary})
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)