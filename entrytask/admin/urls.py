from django.conf.urls import url

from admin.views import event

urlpatterns = [
	url(r'^event/$', event.AdminEventView.as_view(), name='admin-event-view'),
	url(r'^event/(?P<event_id>[0-9]+)/$', event.AdminSingleEventView.as_view(), name='admin-single-event-view'),
	url(r'^event/(?P<event_id>[0-9]+)/uploadImage/$', event.UploadImageView.as_view(), name='admin-upload-image')
]
