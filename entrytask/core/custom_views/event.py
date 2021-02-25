import json

from django.http import JsonResponse
from django.views.generic import View

from core.db_crud.channel import get_all_channels
from core.db_crud.event import get_events, get_event_by_id, insert_event, update_event, delete_event
from core.utils.response import json_response, error_response


class EventView(View):
    def get(self, *args, **kwargs):
        raw_conditions = {
            'start_date__gte': self.request.GET.get('from'),
            'end_date__lte': self.request.GET.get('to'),
            'channel': self.request.GET.get('channel'),
            'location': self.request.GET.get('location')
        }

        base = int(self.request.GET.get('base', 0))
        offset = int(self.request.GET.get('offset', 10))

        filtered_conditions = {k: v for k, v in raw_conditions.items() if v is not None}
        events = get_events(filtered_conditions, base, offset)
        if events is None or len(events) == 0:
            return error_response(404, 'have no event')

        return JsonResponse(events, safe=False)

    def post(self, *args, **kwargs):
        body_json = json.loads(self.request.body)
        print(body_json)
        event = insert_event(body_json)
        if event is None:
            return error_response(400, 'missing data field or wrong data type')
        return json_response(event)


class SingleEventView(View):
    def get(self, *args, **kwargs):
        event_id = int(self.kwargs.get('event_id'))
        event = get_event_by_id(event_id)
        if event is None:
            return error_response(404, 'have no event with id {}'.format(event_id))
        return json_response(event)

    def patch(self, *args, **kwargs):
        event_id = int(self.kwargs.get('event_id'))
        body_json = json.loads(self.request.body)
        event = update_event(event_id, body_json)
        if event is None:
            return error_response(500, 'update failed')
        return json_response(event)

    def delete(self, *args, **kwargs):
        event_id = int(self.kwargs.get('event_id'))
        row_affected = delete_event(event_id)
        if row_affected is None or row_affected[0] == 0:
            return error_response(500, 'delete failed')
        return JsonResponse({'msg': 'deleted event {}'.format(event_id)})


class ChannelView(View):
    def get(self, *args, **kwargs):
        channels = get_all_channels()
        return JsonResponse(channels, safe=False)
