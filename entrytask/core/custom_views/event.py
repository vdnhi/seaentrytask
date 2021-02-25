import json
import time

from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.generic import View
from jsonschema import ValidationError
from jsonschema.validators import validate

from core.db_crud.channel import get_all_channels
from core.db_crud.event import get_events, get_event_by_id, insert_event, update_event, delete_event
from core.db_crud.image import insert_image, insert_image_to_event
from core.db_crud.like import insert_like, get_like_of_event, remove_like
from core.db_crud.participation import get_participation_of_event, insert_participation, remove_participation
from core.db_crud.user import get_user_by_id
from core.schema import event_schema
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
        try:
            validate(body_json, event_schema)
            current_timestamp = int(time.time())
            body_json["create_time"] = current_timestamp
            body_json["update_time"] = current_timestamp
            print(body_json)
            event = insert_event(body_json)
            if event is None:
                return error_response(400, 'missing data field or wrong data type')
            return json_response(event)
        except ValidationError:
            return error_response(400, 'missing data field or wrong data type (exception)')


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


class UploadImageView(View):
    def post(self, *args, **kwargs):
        event_id = int(self.kwargs.get('event_id'))
        incoming_file = self.request.FILES['image']
        filename = default_storage.save(incoming_file.name, incoming_file)
        image_id = insert_image('/media/' + filename)
        insert_image_to_event(event_id, image_id)
        return json_response({'msg': 'upload images successful {}'.format(image_id)})


class LikeEventView(View):
    def get(self, *args, **kwargs):
        event_id = int(self.kwargs.get('event_id'))
        likes = get_like_of_event(event_id)
        users_id = [like.user_id for like in likes]
        user_raw_data = [get_user_by_id(user_id) for user_id in users_id]
        user_data = [{'id': user.id, 'username': user.username} for user in user_raw_data]
        return JsonResponse(user_data, safe=False)

    def post(self, *args, **kwargs):
        event_id = int(self.kwargs.get('event_id'))
        try:
            body_json = json.loads(self.request.body)
            print(body_json)
            validate(body_json, {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'number'},
                    'token': {'type': 'string'}
                },
                'required': ['user_id', 'token']
            })
            insert_like(event_id, body_json["user_id"])
            return json_response({'msg': 'liked'})
        except ValidationError:
            return error_response(400, 'invalid input')

    def delete(self, *args, **kwargs):
        event_id = int(self.kwargs.get('event_id'))
        user_id = self.request.GET.get('user_id')
        token = self.request.GET.get('token')
        row_affected = remove_like(event_id, user_id)
        if row_affected == 0:
            return error_response(404, 'not found')
        return json_response({'msg': 'deleted'})


class ParticipationEventView(View):
    def get(self, *args, **kwargs):
        event_id = int(self.kwargs.get('event_id'))
        list_participant = get_participation_of_event(event_id)
        users_id = [list_participant.user_id for participant in list_participant]
        user_raw_data = [get_user_by_id(user_id) for user_id in users_id]
        user_data = [{'id': user.id, 'username': user.username} for user in user_raw_data]
        return JsonResponse(user_data, safe=False)

    def post(self, *args, **kwargs):
        event_id = int(self.kwargs.get('event_id'))
        try:
            body_json = json.loads(self.request.body)
            print(body_json)
            validate(body_json, {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'number'},
                    'token': {'type': 'string'}
                },
                'required': ['user_id', 'token']
            })
            insert_participation(event_id, body_json["user_id"])
            return json_response({'msg': 'liked'})
        except ValidationError:
            return error_response(400, 'invalid input')

    def delete(self, *args, **kwargs):
        event_id = int(self.kwargs.get('event_id'))
        user_id = self.request.GET.get('user_id')
        token = self.request.GET.get('token')
        row_affected = remove_participation(event_id, user_id)
        if row_affected == 0:
            return error_response(404, 'not found')
        return json_response({'msg': 'deleted'})


class CommentEventView(View):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass
