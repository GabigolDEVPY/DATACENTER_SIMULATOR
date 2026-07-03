from django.urls import path
from .views.views import HomeView, GetBayDetail
from .views.bays_views import ChangeStatusBay

app_name = "server"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    
    
    # bays
    path('get-bay-detail/<int:id>', GetBayDetail.as_view(), name="get_bay_detail"),
    path('bay-status-changed/<int:id>', ChangeStatusBay.as_view(), name="change_status_bay")
]


