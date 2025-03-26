from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
