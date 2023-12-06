from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MonApplication.urls')),
    path('pokedex/', include('MonApplication.urls')),
    path('team/', include('MonApplication.urls')),
]