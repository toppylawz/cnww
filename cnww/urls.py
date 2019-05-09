from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import cnewsww.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cnewsww.views.home, name='home'),
    path('articles/', include('articles.urls'))
]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
