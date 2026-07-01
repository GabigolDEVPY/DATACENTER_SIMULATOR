from django.urls import path
from .views import HomeView, GetBayDetail

app_name = "datacenter"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('get-bay-detail/<int:id>', GetBayDetail.as_view(), name="get_bay_detail")
]


