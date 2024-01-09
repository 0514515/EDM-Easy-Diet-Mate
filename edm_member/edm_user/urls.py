from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
    path('api/',include('subscribe.urls')),
    path('api/',include('board.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)