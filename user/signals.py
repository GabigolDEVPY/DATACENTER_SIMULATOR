from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver

from server.models import Bay, Rack
from user.models import Inventory, User


@receiver(post_save, sender=User)
def create_user_resources(sender, instance, created, **kwargs):
	if not created:
		return

	instance.money = Decimal("10000.00")
	instance.save(update_fields=["money"])

	inventory, _ = Inventory.objects.get_or_create(user=instance)
	rack, _ = Rack.objects.get_or_create(
		user=instance,
		name="Rack 1",
		defaults={"bay": 1},
	)
	Bay.objects.get_or_create(name="Bay 1", rack=rack)
