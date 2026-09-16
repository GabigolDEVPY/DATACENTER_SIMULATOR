from user.services.inventory_services import InventoryService
from server.services.bay_service import BayService

class BayContextService:
    @staticmethod
    def get_bay_model_context(user_id, bay_id):
        bay = BayService(bay_id=bay_id).get_view_model()
        components = InventoryService(user_id).get_components()
        return bay, components
    
    @staticmethod
    def change_component(data, user_id, bay_id):
        components = InventoryService(user_id).get_components()
        bay = BayService(bay_id=bay_id).change_component(data)
        return bay, components
        
    @staticmethod
    def change_status(user_id, bay_id):
        bay = BayService(bay_id).change_status()
        components = InventoryService(user_id).get_components()
        return bay, components
    
    @staticmethod
    def remove_component(data, user_id, bay_id):
        bay = BayService(bay_id).remove_component(data)
        components = InventoryService(user_id).get_components()
        return bay, components
        
    
        
        