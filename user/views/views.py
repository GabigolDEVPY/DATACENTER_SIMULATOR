from django.views.generic import View
from ..services.services import UserService
from django.http import JsonResponse



        
class GetBalanceView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            UserService.refresh_balance(user)
            return JsonResponse({"balance": str(user.money)})
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)