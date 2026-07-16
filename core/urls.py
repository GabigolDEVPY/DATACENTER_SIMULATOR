from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('server/', include('server.urls')),
    path('shop/', include('shop.urls')),
    path('user/', include('user.urls'))
]
