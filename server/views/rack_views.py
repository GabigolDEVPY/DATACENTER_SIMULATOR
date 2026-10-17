from django.views import View
from server.models import Rack
from django.http import JsonResponse



class RemoveRack(View):
    def post(self, request, id):
        try:
            rack = Rack.objects.get(id=id)
            rack.is_active = False
            rack.save()
            return JsonResponse({"message": "Rack removed successfully."}, status=200)
        except Rack.DoesNotExist:
            return JsonResponse({"error": "Rack not found."}, status=404)