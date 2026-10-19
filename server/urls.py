from django.urls import path
from .views.views import HomeView
from .views.bays_views import ChangeStatusBay, GetBayDetail, ChangeComponent, RemoveComponent
from .views.rack_views import RemoveRack, InstallRack, InstallBay, RemoveBay
from .views.datacenter_views import DatacenterUpgradeView

app_name = "server"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    
    
    # bays -modal
    path('get-bay-detail/<int:id>', GetBayDetail.as_view(), name="get_bay_detail"),
    path('bay-status-changed/<int:id>', ChangeStatusBay.as_view(), name="change_status_bay"),
    path('bay-component-changed/<int:id>', ChangeComponent.as_view(), name="change_component_bay"),
    path('bay-component-remove/<int:id>', RemoveComponent.as_view(), name="remove_component_bay"),
    
    # api/
    path('api/rack/remove/', RemoveRack.as_view(), name="remove_rack"),
    path('api/rack/install/', InstallRack.as_view(), name="install_rack"),
    
    path('api/bay/remove/', RemoveBay.as_view(), name="remove_bay"),
    path('api/bay/install/', InstallBay.as_view(), name="install_bay"),
    
    path('datacenter/upgrade/', DatacenterUpgradeView.as_view(), name="upgrade_datacenter"),
]


