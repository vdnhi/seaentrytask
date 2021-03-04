from django.views.generic.base import View

from commonlib.constant import PAGING_SIZE
from commonlib.db_crud.channel import get_channels
from commonlib.utils.decorator import error_handler
from commonlib.utils.response import json_response


class ChannelView(View):
	@error_handler
	def get(self, *args, **kwargs):
		base = int(self.request.GET.get('base', 0))
		offset = min(int(self.request.GET.get('offset', PAGING_SIZE)), PAGING_SIZE)
		channels = get_channels(base, offset)
		return json_response(data=channels)
