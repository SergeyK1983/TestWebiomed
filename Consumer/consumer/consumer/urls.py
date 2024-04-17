from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += doc_urls  # swagger

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = page_not_found
# handler500 = server_error

