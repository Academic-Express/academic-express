import requests
from django.conf import settings


class FeedEngineSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers.update({
            'Authorization': f'Bearer {settings.FEED_ENGINE_TOKEN}',
        })

    def request(self, method, url, *args, **kwargs):
        joined_url = f'{settings.FEED_ENGINE_URL}{url}'
        return super().request(method, joined_url, *args, **kwargs)


session = FeedEngineSession()
