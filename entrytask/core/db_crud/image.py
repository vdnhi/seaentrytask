from core.models import Image, EventImageMapping


def insert_image(image_url):
    image = Image.objects.create(image_url=image_url)
    return image.id


def insert_image_to_event(event_id, image_id):
    mapping = EventImageMapping.objects.create(event_id=event_id, image_id=image_id)
    return mapping
