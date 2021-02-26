from django.forms.models import model_to_dict

from core.models import Comment


def get_event_comments(event_id, base, offset):
    comments = list(Comment.objects.filter(event_id=event_id).order_by('-create_time'))[base: base + offset]
    comments = [model_to_dict(comment) for comment in comments]
    return comments


def insert_comment(data):
    comment = Comment.objects.create(**data)
    return comment.id
