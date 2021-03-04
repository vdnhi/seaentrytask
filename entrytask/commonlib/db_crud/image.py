from commonlib.models import Image, EventImageMapping


def insert_image(image_url):
	image = Image.objects.create(image_url=image_url)
	return image.id


def insert_image_to_event(event_id, image_id):
	mapping = EventImageMapping.objects.create(event_id=event_id, image_id=image_id)
	return mapping


def get_image_url_by_ids(image_ids):
	lst = list(Image.objects.filter(id__in=image_ids).values_list('id', 'image_url'))
	mapping = {}
	for image in lst:
		mapping[image[0]] = image[1]
	return mapping


def get_events_images(event_ids):
	list_mapping = EventImageMapping.objects.filter(event_id__in=event_ids).values_list('image_id', 'event_id')
	list_image_id = []
	image_existed = {}
	result = {}
	for item in list_mapping:
		image_id = item[0]
		event_id = item[1]

		if image_id not in image_existed:
			list_image_id.append(image_id)
			image_existed[image_id] = True

		if event_id not in result:
			result[event_id] = [image_id]
		else:
			result[event_id].append(image_id)

	image_urls = get_image_url_by_ids(list_image_id)
	for _, item in result.items():
		for i in range(len(item)):
			item[i] = image_urls[item[i]]
	return result
