from django.urls import path, include
from app.views import home


urlpatterns = [
    path('', home),
    path('api/v1/', include('app.api.urls')),
]
