from model.viewmodels.ia_model_view_model import IaModelViewModel
from model.viewmodels.bay_option_view_model import BayOption
from model.services.model_service import ModelService
from server.models import Bay
from server.services.bay_service import BayService
from model.models import AIInstanceBay
import math



def get_max_instances_avaliable(bay, model):
    vram = bay.get_total_vram()
    ram = bay.get_total_ram()
    ia_allocations = bay.get_ai_allocations()
    
    for ia_model in ia_allocations:
        ia_model = ia_model.ai_instance.model
        vram -= ia_model.gpu_vram
        ram -= ia_model.ram_gb
        
    ram_times = math.floor( vram / model.ram_gb)
    vram_times = math.floor( vram / model.gpu_vram)
    
    times = min(ram_times, vram_times)
    print(times)
    
    # return ia_allocations
    return times
    


class IaModelContextServices:
    @staticmethod
    def get_ia_models(user_id):
        service = ModelService(user_id=user_id)
        user_ia_models = [
            IaModelViewModel.from_model(item.model, status=item.status)
            for item in service.get_user_models() 
            ]
        
        available_ia_models = [
            IaModelViewModel.from_model(model, status="stopped")
            for model in service.get_available_models()
        ]
        
        return {"user_ia_models": user_ia_models, "ia_models": available_ia_models}
    
    
    
    @staticmethod
    def get_ia_model(user_id, model_id):
        context = {}
        service = ModelService(user_id)
        ia_model = service.get_user_model(model_id)

        if ia_model:
            model_view = IaModelViewModel.from_model(ia_model.model, status=ia_model.status)
            if model_view.status == "not_installed":
                context["bays_avaliable"] = []
                
                bays = Bay.objects.filter(rack__user_id=user_id)
                for bay in bays:
                    bay_mod = BayService(bay.id)
                    model_view_alocatte = bay_mod.get_allocate_space_storage()
                    bay_storage_availabe = bay_mod.get_total_storage() - model_view_alocatte
                    if bay_storage_availabe >= model_view.storage_gb:
                        context["bays_avaliable"].append(bay)
                        
                        
            elif model_view.status == "stopped":
                context["bays_avaliable"] = []
                
                bays = Bay.objects.filter(rack__user_id=user_id)
                for bay in bays:
                    bay_mod = BayService(bay.id)
                    max_instances = get_max_instances_avaliable(bay_mod, model_view)
                    model_view_alocatte = bay_mod.get_allocate_space_storage()
                    bay_storage_availabe = bay_mod.get_total_storage() - model_view_alocatte
                    if bay_storage_availabe >= model_view.storage_gb:
                        context["bays_avaliable"].append(BayOption(bay, max_instances))
                
            
        else:
            model = service.get_model_or_404(model_id)
            model_view = IaModelViewModel.from_model(model, status=None)        
            
                
        context["model"] = model_view
        return context
    