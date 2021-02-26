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
from django.conf.urls.static import static
from django.views.static import serve

from core import views as core_view
from core.custom_views import event, user
from entrytask import settings

urlpatterns = [
    url(r'test/$', core_view.test),
    url(r'event/(?P<event_id>[0-9]+)/$', event.SingleEventView.as_view(), name='specific-event'),
    url(r'event/(?P<event_id>[0-9]+)/uploadImage/$', event.UploadImageView.as_view(), name='upload-image'),
    url(r'event/(?P<event_id>[0-9]+)/like/$', event.LikeEventView.as_view(), name='like-event'),
    url(r'event/(?P<event_id>[0-9]+)/participation/$', event.ParticipationEventView.as_view(),
        name='participation-event'),
    url(r'event/(?P<event_id>[0-9]+)/comment/$', event.CommentEventView.as_view(), name='comment-event'),
    url(r'event/channel/$', event.ChannelView.as_view(), name='event-channel'),
    url(r'event/$', event.EventView.as_view(), name='event'),
    url(r'user/register/$', user.UserRegisterView.as_view(), name='user-register'),
    url(r'user/prelogin/$', user.UserPreloginView.as_view(), name='user-prelogin'),
    url(r'user/login/$', user.UserLoginView.as_view(), name='user-login'),
    url(r'user/logout/$', user.UserLogoutView.as_view(), name='user-logout'),
    url(r'user/(?P<user_id>[0-9]+)/$', user.UserView.as_view(), name='user'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
