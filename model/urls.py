from django.urls import path
from .views import HomeView, IAModelDetailView, IaModelRun, IaModelInstall

app_name = "model"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    path("ia-detail/<int:id>", IAModelDetailView.as_view(), name="get_ia_detail"),
    path("ia_model_run/<int:id>", IaModelRun.as_view(), name="ia_model_run"),
    path("ia_model_install/", IaModelInstall.as_view(), name="ia_model_install")
    
    
]


