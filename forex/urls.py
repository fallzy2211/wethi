from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from users.views import  dashboard

urlpatterns = [
    path("", dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('django.contrib.auth.urls')),  # URLs d'authentification de Django

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)