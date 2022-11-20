from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urls = [
    path("rooms/", include("rooms.urls")),
    path("categories/", include("categories.urls")),
    path("experiences/", include("experiences.urls")),
    path("medias/", include("medias.urls")),
]

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # version 1
    path("api/v1/", include(urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
