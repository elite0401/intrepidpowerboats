import urllib.parse

import requests
from django.conf import settings


class Builder:
    def __init__(self, vimeo_api_url, access_token):
        self._vimeo_api_url = vimeo_api_url
        self._access_token = access_token

    def create_ticket(self):
        params = urllib.parse.urlencode({"type": "streaming"}, doseq=True)
        headers = {"Authorization": "Bearer %s" % self.get_token()}
        full_url = "%s?%s" % (self.get_my_video_url(), params)
        return requests.post(full_url, headers=headers).json()

    def finish_upload(self, ticket_id, user=None):
        instance = self.get_instance(ticket_id, user)
        headers = {"Authorization": "Bearer %s" % self.get_token()}

        self.verify(instance.upload_link_secure)

        full_url = self.get_complete_url(instance.complete_uri)
        response = requests.delete(full_url, headers=headers)
        response.raise_for_status()
        try:
            self.set_video_id(instance, response.headers.get('location').replace('/videos/', ''))
        except AttributeError:
            pass
        self.set_to_completed(instance)
        instance.save()

    def get_instance(self, ticket_id, user):
        raise NotImplementedError('should be implemented by subclasses')

    def get_text_field_for(self, instance):
        raise NotImplementedError('should be implemented by subclasses')

    def set_video_id(self, instance, vimeo_video_id):
        raise NotImplementedError('should be implemented by subclasses')

    def save_thumbnail(self, instance, filename, thumbnail_file):
        raise NotImplementedError('should be implemented by subclasses')

    def set_to_completed(self, instance):
        raise NotImplementedError('should be implemented by subclasses')

    def get_token(self):
        return self._access_token

    def get_my_video_url(self):
        return urllib.parse.urljoin(self._vimeo_api_url, 'me/videos/')

    @classmethod
    def default(cls):
        url = settings.VIMEO_CONFIG['VIMEO_API_URL']
        token = settings.VIMEO_CONFIG['PRO_UPLOAD_TOKEN']
        return cls(url, token)

    def get_complete_url(self, complete_uri):
        return urllib.parse.urljoin(self._vimeo_api_url, complete_uri)

    def verify(self, upload_link_secure):
        headers = {"Authorization": "Bearer %s" % self.get_token(), "Content-Range": "bytes */*"}
        response = requests.put(upload_link_secure, headers=headers)
        response.raise_for_status()
