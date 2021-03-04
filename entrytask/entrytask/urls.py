from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.static import serve

import admin.urls
import api.urls
from entrytask import settings

urlpatterns = [
	url(r'^api/', include(api.urls)),
	url(r'^admin/', include(admin.urls)),
	url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
