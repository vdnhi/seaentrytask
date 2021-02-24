"""entrytask URL Configuration

The `urlpatterns` list routes URLs to custom_views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function custom_views
    1. Add an import:  from my_app import custom_views
    2. Add a URL to urlpatterns:  url(r'^$', custom_views.home, name='home')
Class-based custom_views
    1. Add an import:  from other_app.custom_views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from core import views as core_view
from core.custom_views import event

urlpatterns = [
    url(r'test/$', core_view.test),
    url(r'event/(?P<event_id>[0-9]+)/$', event.SingleEventView.as_view(), name='specific-event'),
    url(r'event/$', event.EventView.as_view(), name='event'),
]
