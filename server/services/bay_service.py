from django.db import transaction
from django.shortcuts import get_object_or_404

from server.models import Bay, StorageAllocation
from server.viewmodels.bay_viewmodel import BayViewModel
from user.models import InventoryItem


class BayError(Exception):
    """Erro de regra de negócio relacionado à Bay."""


class BayService:
    COMPONENT_FIELDS = {
        "cpu": "cpu",
        "ssd": "ssd",
        "gpu1": "gpu",
        "gpu2": "gpu",
        "gpu3": "gpu",
        "ram1": "ram",
        "ram2": "ram",
        "ram3": "ram",
    }

    SELECT_RELATED = [
        f"{field}__item__{kind}" for field, kind in COMPONENT_FIELDS.items()
    ]

    def __init__(self, bay=None, bay_id=None):
        """Aceita uma Bay já carregada (evita query extra) ou um id."""
        if bay is None:
            bay = get_object_or_404(
                Bay.objects.select_related(*self.SELECT_RELATED), id=bay_id
            )
        self.bay = bay
        self._components = None

    # ---------- Componentes ----------

    def _get_component(self, field):
        """Retorna o componente concreto (cpu/ssd/gpu/ram) de um slot."""
        slot = getattr(self.bay, field)
        if not slot:
            return None
        return getattr(slot.item, self.COMPONENT_FIELDS[field])

    @property
    def components(self):
        if self._components is None:
            self._components = [
                c for c in (self._get_component(f) for f in self.COMPONENT_FIELDS)
                if c is not None
            ]
        return self._components

    def _invalidate_components(self):
        self._components = None

    def _sum(self, attr):
        return sum(getattr(c, attr, 0) or 0 for c in self.components)

    # ---------- Totais ----------

    def get_total_watts(self):
        return self._sum("watts")

    def get_total_price(self):
        return self._sum("price")

    def get_total_ram(self):
        return self._sum("ram_gb")

    def get_total_vram(self):
        return self._sum("vram")

    def get_total_processors(self):
        cpu = self._get_component("cpu")
        return cpu.cores if cpu else 0

    def get_total_storage(self):
        ssd = self._get_component("ssd")
        return ssd.ssd_gb if ssd else 0

    # ---------- Storage ----------
    def allocate_space_for_model(self, ia_model, allocated_gb):
        StorageAllocation.objects.create(bay=self.bay, ai_model=ia_model, allocated_gb=allocated_gb)
        

    def get_allocate_space_storage(self):
        return sum(a.allocated_gb for a in self.get_storage_allocations())

    def get_free_storage(self):
        return self.get_total_storage() - self.get_allocate_space_storage()

    def get_storage_percentage(self):
        total = self.get_total_storage()
        if total == 0:
            return "0.00"
        return f"{(self.get_allocate_space_storage() / total) * 100:.2f}"

    def get_storage_allocations(self):
        return self.bay.storage_allocations.all()

    def has_storage_for(self, storage_gb):
        return self.get_free_storage() >= storage_gb

    # ---------- IA ----------

    def get_ai_allocations(self):
        return self.bay.ai_allocations.select_related("ai_instance__model")

    def get_free_resources(self):
        """RAM e VRAM livres depois de descontar as instâncias já alocadas."""
        vram = self.get_total_vram()
        ram = self.get_total_ram()

        for allocation in self.get_ai_allocations():
            model = allocation.ai_instance.model
            vram -= model.gpu_vram
            ram -= model.ram_gb

        return max(ram, 0), max(vram, 0)

    def get_max_instances_available(self, model):
        """Quantas instâncias de `model` ainda cabem nesta bay."""
        free_ram, free_vram = self.get_free_resources()

        limits = []
        if model.ram_gb:
            limits.append(free_ram // model.ram_gb)
        if model.gpu_vram:
            limits.append(free_vram // model.gpu_vram)

        return int(min(limits)) if limits else 0

    # ---------- Ações ----------

    def _validate_slot(self, field):
        if field not in self.COMPONENT_FIELDS:
            raise BayError(f"Slot inválido: {field}")

    def _ensure_inactive(self):
        if self.bay.is_active:
            raise BayError("Desligue a bay antes de alterar componentes.")

    def change_status(self):
        self.bay.is_active = not self.bay.is_active
        self.bay.save(update_fields=["is_active"])

    def change_component(self, field, component_id, user_id):
        self._validate_slot(field)
        self._ensure_inactive()

        with transaction.atomic():
            new_component = get_object_or_404(
                InventoryItem,
                id=component_id,
                is_equiped=False,
                user_id=user_id,  # ajuste o nome do campo conforme seu model
            )

            self._unequip(getattr(self.bay, field))

            new_component.is_equiped = True
            new_component.save(update_fields=["is_equiped"])

            setattr(self.bay, field, new_component)
            self.bay.save(update_fields=[field])

        self._invalidate_components()

    def remove_component(self, field):
        self._validate_slot(field)
        self._ensure_inactive()

        with transaction.atomic():
            self._unequip(getattr(self.bay, field))
            setattr(self.bay, field, None)
            self.bay.save(update_fields=[field])

        self._invalidate_components()

    @staticmethod
    def _unequip(item):
        if item:
            item.is_equiped = False
            item.save(update_fields=["is_equiped"])

    # ---------- ViewModel ----------

    def get_view_model(self):
        return BayViewModel(
            id=self.bay.id,
            name=self.bay.name,
            is_active=self.bay.is_active,
            **{field: self._get_component(field) for field in self.COMPONENT_FIELDS},
            total_watts=self.get_total_watts(),
            total_price=self.get_total_price(),
            total_ram=self.get_total_ram(),
            total_vram=self.get_total_vram(),
            total_processors=self.get_total_processors(),
            total_storage=self.get_total_storage(),
            allocate_storage=self.get_allocate_space_storage(),
            storage_allocations=self.get_storage_allocations(),
            storage_percentage=self.get_storage_percentage(),
        )