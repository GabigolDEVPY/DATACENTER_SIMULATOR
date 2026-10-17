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
        

class InstallBay(View):
    def post(self, request):
        bay_id = request.POST.get("id")
        position = request.POST.get("position")
        rack_id = request.POST.get("rack_id")
        print(f"Rack ID for bay installation: {rack_id}")  # Debugging line
        print(f"Bay ID to install: {bay_id}")  # Debugging line
        try:
            bay = Bay.objects.get(id=bay_id)
            bay.is_selected = True
            bay.position = position
            bay.rack_id = rack_id
            bay.save(update_fields=["is_selected", "position", "rack_id"])
            return JsonResponse({"message": "Bay installed successfully."}, status=200)
        except Bay.DoesNotExist:
            return JsonResponse({"error": "Bay not found."}, status=404)
    
    
class RemoveBay(View):
    def post(self, request):
        bay_id = request.POST.get("id")
        print(f"Bay ID to remove: {bay_id}")  # Debugging line
        try:
            bay = Bay.objects.get(id=bay_id)
            bay.is_selected = False
            bay.position = 0
            bay.rack = None
            bay.save(update_fields=["is_selected", "position", "rack"])
            return JsonResponse({"message": "Bay removed successfully."}, status=200)
        except Bay.DoesNotExist:
            return JsonResponse({"error": "Bay not found."}, status=404)