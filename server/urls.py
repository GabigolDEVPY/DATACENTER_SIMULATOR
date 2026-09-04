from django.urls import path
from .views.views import HomeView
from .views.bays_views import ChangeStatusBay, GetBayDetail, ChangeComponent

app_name = "server"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    
    
    # bays
    path('get-bay-detail/<int:id>', GetBayDetail.as_view(), name="get_bay_detail"),
    path('bay-status-changed/<int:id>', ChangeStatusBay.as_view(), name="change_status_bay"),
    path('bay-component-changed/<int:id>', ChangeComponent.as_view(), name="change_component_bay"),
]


