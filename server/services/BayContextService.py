from server.services.bay_service import BayService
from server.viewmodels.bay_viewmodel import BayViewModel
from user.services.inventory_services import InventoryService

class BayContextService:

    @staticmethod
    def _build_bay_view_model(service):
        return BayViewModel(
            id=service.bay.id,
            name=service.bay.name,
            is_active=service.bay.is_active,

            **{
                field: service._get_component(field)
                for field in service.COMPONENT_FIELDS
            },

            total_watts=service.get_total_watts(),
            total_price=service.get_total_price(),
            total_ram=service.get_total_ram(),
            total_vram=service.get_total_vram(),
            total_processors=service.get_total_processors(),
            total_storage=service.get_total_storage(),

            allocate_storage=service.get_allocate_space_storage(),
            storage_allocations=service.get_storage_allocations(),
            storage_percentage=service.get_storage_percentage(),
        )
        

    @classmethod
    def get_bay_context(cls, user_id, bay_id):

        service = BayService(bay_id=bay_id)
        bay_view_model = cls._build_bay_view_model(service)
        components = (InventoryService(user_id).get_components())
        
        return {"bay": bay_view_model,**components}
    