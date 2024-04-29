from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('lessons/', include('projects.urls')),
    path('', include('users.urls')),
    path('quizes/', include('quizes.urls', namespace='quizes')),
    path('results/', include('results.urls', namespace='results')),
]
# URL pattern to have access to the static files in the web application (images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
