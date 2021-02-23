from core.models import Comment


def get_event_comments(event_id):
    comments = Comment.objects.filter(event_id=event_id).order_by('create_time')
    return comments