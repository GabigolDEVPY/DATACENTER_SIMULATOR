from django.views import View
from server.models import Rack, Bay
from django.http import JsonResponse



class RemoveRack(View):
    def post(self, request):
        rack_id = request.POST.get("id")
        print(f"Rack ID to remove: {rack_id}")  # Debugging line
        try:
            rack = Rack.objects.get(id=rack_id)
            rack.is_selected = False
            position = 0
            rack.save(update_fields=["is_selected", "position"])
            return JsonResponse({"message": "Rack removed successfully."}, status=200)
        except Rack.DoesNotExist:
            return JsonResponse({"error": "Rack not found."}, status=404)
        

class InstallRack(View):
    def post(self, request):
        rack_id = request.POST.get("id")
        rack_position = request.POST.get("position")
        print(f"Rack ID to install: {rack_id}")  # Debugging line
        try:
            rack = Rack.objects.get(id=rack_id)
            rack.is_selected = True
            rack.position = rack_position
            rack.save(update_fields=["is_selected", "position"])
            for bay in rack.bays.all():
                bay.is_selected = True
                bay.save(update_fields=["is_selected"])
            return JsonResponse({"message": "Rack installed successfully."}, status=200)
        except Rack.DoesNotExist:
            return JsonResponse({"error": "Rack not found."}, status=404)