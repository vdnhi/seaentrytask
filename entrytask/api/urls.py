from django.conf.urls import url
from django.views.static import serve

from api.views import like, participation, comment, channel, event, user
from entrytask import settings

urlpatterns = [
	url(r'^event/(?P<event_id>[0-9]+)/$', event.ApiSingleEventView.as_view(), name='api-single-event-view'),
	url(r'^event/(?P<event_id>[0-9]+)/like/$', like.LikeEventView.as_view(), name='like-event'),
	url(r'^event/(?P<event_id>[0-9]+)/participation/$', participation.ParticipationEventView.as_view(),
	    name='participation-event'),
	url(r'^event/(?P<event_id>[0-9]+)/comment/$', comment.CommentEventView.as_view(), name='comment-event'),
	url(r'^event/channel/$', channel.ChannelView.as_view(), name='event-channel'),
	url(r'^event/$', event.ApiEventView.as_view(), name='event'),
	url(r'^user/register/$', user.UserRegisterView.as_view(), name='user-register'),
	url(r'^user/prelogin/$', user.UserPreloginView.as_view(), name='user-prelogin'),
	url(r'^user/login/$', user.UserLoginView.as_view(), name='user-login'),
	url(r'^user/logout/$', user.UserLogoutView.as_view(), name='user-logout'),
	url(r'^user/(?P<user_id>[0-9]+)/$', user.UserView.as_view(), name='user'),
	url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]
