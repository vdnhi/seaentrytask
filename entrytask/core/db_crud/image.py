from core.models import Image, EventImageMapping


def insert_image(image_url):
    image = Image.objects.create(image_url=image_url)
    return image.id


def insert_image_to_event(event_id, image_id):
    mapping = EventImageMapping.objects.create(event_id=event_id, image_id=image_id)
    return mapping


def get_image_url_by_id(image_id):
    image = Image.objects.filter(id=image_id).first()
    return image.image_url


def get_event_images(event_id):
    list_mapping = EventImageMapping.objects.filter(event_id=event_id)
    return [get_image_url_by_id(mapping.image_id) for mapping in list_mapping]
