from django.urls import path
from .views import HomeView, IAModelDetailView

app_name = "model"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    path("ia-detail/<int:id>", IAModelDetailView.as_view(), name="get_ia_detail")
    
]


