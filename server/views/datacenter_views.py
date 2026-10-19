from django.views import View
from server.models import Rack, Bay
from django.http import JsonResponse


class DatacenterUpgradeView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        datacenter = user.datacenter.first()

        if datacenter and datacenter.updates < 4:
            price = 10000 * (datacenter.updates + 1)  # Example price calculation
            if user.money < price:
                return JsonResponse({"error": "Insufficient funds for upgrade."}, status=400)
            datacenter.updates += 1
            datacenter.save(update_fields=['updates'])
            return JsonResponse({"message": "Datacenter upgraded successfully."}, status=200)
        else:
            return JsonResponse({"error": "Datacenter not found or maximum upgrades reached."}, status=404)