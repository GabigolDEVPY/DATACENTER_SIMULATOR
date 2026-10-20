from django.views.generic import View
from ..services.services import UserService
from ..services.inventory_services import InventoryService
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from server.models import Rack, Bay
from user.models import InventoryItem

        
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
        


RACK_PRICE = 1000  # mesmo valor usado em get_inventory_summary
BAY_PRICE = 1000

HARDWARE_FIELDS = {
    "cpu": "item__cpu__isnull",
    "gpu": "item__gpu__isnull",
    "ram": "item__ram__isnull",
    "ssd": "item__ssd__isnull",
}


def credit_user(user, amount):
    """
    ADAPTE AQUI para o seu modelo de dinheiro.
    Exemplo assumindo um campo `money` no usuário.
    """
    type(user).objects.filter(pk=user.pk).update(money=F("money") + amount)
    user.refresh_from_db(fields=["money"])
    return user.money


def _sell_rack(user, item_id):
    rack = (
        Rack.objects.select_for_update()
        .filter(id=item_id, user_id=user.id, is_selected=False)
        .first()
    )
    if not rack:
        raise LookupError("Rack não encontrado.")
    if rack.bays.exists():
        raise ValueError("Remova as baias do rack antes de vendê-lo.")
    price = RACK_PRICE
    rack.delete()
    return price


def _sell_bay(user, item_id):
    bay = (
        Bay.objects.select_for_update()
        .filter(id=item_id, user=user.id, is_selected=False)
        .first()
    )
    if not bay:
        raise LookupError("Baia não encontrada.")
    price = BAY_PRICE
    bay.delete()
    return price


def _sell_hardware(user, item_id, item_type):
    item = (
        InventoryItem.objects.select_for_update()
        .select_related("item")
        .filter(
            id=item_id,
            inventory__user=user.id,
            is_equiped=False,
            **{HARDWARE_FIELDS[item_type]: False},
        )
        .first()
    )
    if not item:
        raise LookupError("Item não encontrado.")
    price = item.item.price
    item.delete()
    return price


class SellItemView(LoginRequiredMixin, View):
    def post(self, request):
        item_type = (request.POST.get("type") or "").lower()
        raw_id = request.POST.get("id")

        try:
            item_id = int(raw_id)
        except (TypeError, ValueError):
            return JsonResponse({"error": "ID inválido."}, status=400)

        if item_type not in ("rack", "bay", *HARDWARE_FIELDS):
            return JsonResponse({"error": "Tipo de item inválido."}, status=400)

        try:
            with transaction.atomic():
                if item_type == "rack":
                    price = _sell_rack(request.user, item_id)
                elif item_type == "bay":
                    price = _sell_bay(request.user, item_id)
                else:
                    price = _sell_hardware(request.user, item_id, item_type)

                balance = credit_user(request.user, price)
        except LookupError as e:
            return JsonResponse({"error": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse({"success": True, "sold": price, "balance": balance})