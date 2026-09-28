from user.services.inventory_services import InventoryService
from server.services.bay_service import BayService

class BayApplicationService:
    def _build_context(bay_view_model, user_id):
        components = InventoryService(user_id).get_components()
        return {"bay": bay_view_model, **components}
    
    @staticmethod
    def get_bay_model_context(user_id, bay_id):
        view_model = BayService(bay_id=bay_id).get_view_model()
        return BayApplicationService._build_context(view_model, user_id)
    
    @staticmethod
    def change_component(data, user_id, bay_id):
        service = BayService(bay_id=bay_id)
        service.change_component(data)
        return BayApplicationService._build_context(service.get_view_model(), user_id)
        
    @staticmethod
    def change_status(user_id, bay_id):
        service = BayService(bay_id)
        service.change_status()
        return BayApplicationService._build_context(service.get_view_model(), user_id)
    
    @staticmethod
    def remove_component(data, user_id, bay_id):
        service = BayService(bay_id)
        service.remove_component(data)
        return BayApplicationService._build_context(service.get_view_model(), user_id)

        