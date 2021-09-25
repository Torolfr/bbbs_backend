import os

import requests
from django.conf import settings
from django.utils.timezone import now


class ImageFromUrlMixin:
    def load_image(self, *, image_url, save=False):
        new_id = str(now().timestamp())
        directory = self.__class__.image.field.upload_to
        try:
            response = requests.get(image_url)
            if not os.path.isdir(settings.MEDIA_ROOT / f'{directory}'):
                os.mkdir(settings.MEDIA_ROOT / f'{directory}')
            with open(
                settings.MEDIA_ROOT / f'{directory}/{new_id}_pic.jpg',
                'wb'
            ) as image:
                image.write(response.content)
                self.image = f'{directory}/{new_id}_pic.jpg'
            if save:
                self.save()
        except requests.exceptions.ConnectionError:
            pass
