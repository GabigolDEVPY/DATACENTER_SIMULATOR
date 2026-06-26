from django.urls import path
from .views import HomeView, SendView

appname = 'notify'

urlpatterns = [
    path('home/', HomeView.as_view()),
    path('send/', SendView.as_view()),
]