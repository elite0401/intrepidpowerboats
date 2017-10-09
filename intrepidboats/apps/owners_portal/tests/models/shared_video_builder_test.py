from django.test import TestCase
from faker import Factory
from mock import patch
from nose.tools import assert_equals
from nose.tools import assert_false
from nose.tools import assert_true
from nose.tools import istest

from intrepidboats.libs.fixtures.user import a_user
from ...models import SharedVideoBuilder, SharedVideo

fake = Factory.create()


class SharedVideoTestMixin:
    def json_response(self, data):
        class JsonResponse:
            def __init__(self, data):
                self._data = data

            def json(self):
                return self._data

            def raise_for_status(self):
                pass

        return JsonResponse(data)

    def fake_response(self, **kwargs):
        return self.json_response(self.fake_data(**kwargs))

    def fake_data(self, **kwargs):
        default = {
            "uri": fake.uri_path(deep=None),
            "complete_uri": fake.uri_path(deep=None),
            "ticket_id": fake.pystr(min_chars=10, max_chars=20),
            "user": fake.simple_profile(),
            "upload_link_secure": fake.uri(),
        }
        return {
            **default,
            **kwargs,
        }


class TestSharedVideoCreation(SharedVideoTestMixin, TestCase):
    def setUp(self):
        self.user = a_user()
        self.url = "https://example.com"
        self.token = "xxxxxxxxxxxxxxxxx"
        self.builder = SharedVideoBuilder(
            self.url,
            self.token
        )

    @istest
    def create_based_on_data(self):
        data = self.fake_response()
        with patch("requests.post", return_value=data):
            self.builder.create_video(self.user)
        assert_equals(1, SharedVideo.objects.count())

    @istest
    def create_for_user(self):
        data = self.fake_response()
        with patch("requests.post", return_value=data):
            self.builder.create_video(self.user)
        assert_equals(1, self.user.shared_media.count())

    @istest
    def create_with_ticket_id(self):
        ticket_id = fake.pystr(min_chars=10, max_chars=20)
        data = self.fake_response(ticket_id=ticket_id)
        with patch("requests.post", return_value=data):
            self.builder.create_video(self.user)
        video = SharedVideo.objects.last()

        assert_equals(ticket_id, video.ticket_id)

    @istest
    def create_with_uri(self):
        uri = fake.uri_path(deep=None)
        data = self.fake_response(uri=uri)
        with patch("requests.post", return_value=data):
            self.builder.create_video(self.user)
        video = SharedVideo.objects.last()

        assert_equals(uri, video.uri)

    @istest
    def create_with_vimeo_user(self):
        vimeo_user = fake.simple_profile()
        data = self.fake_response(user=vimeo_user)
        with patch("requests.post", return_value=data):
            self.builder.create_video(self.user)
        video = SharedVideo.objects.last()

        assert_equals(str(vimeo_user), video.vimeo_user)

    @istest
    def create_with_upload_link_secure(self):
        link = fake.uri()
        data = self.fake_response(upload_link_secure=link)
        with patch("requests.post", return_value=data):
            self.builder.create_video(self.user)
        video = SharedVideo.objects.last()

        assert_equals(link, video.upload_link_secure)

    @istest
    def create_with_complete_url(self):
        uri = fake.uri_path(deep=None)
        data = self.fake_response(complete_uri=uri)
        with patch("requests.post", return_value=data):
            self.builder.create_video(self.user)
        video = SharedVideo.objects.last()

        assert_equals(uri, video.complete_uri)

    @istest
    def videos_are_not_completed_by_default(self):
        data = self.fake_response()
        with patch("requests.post", return_value=data):
            self.builder.create_video(self.user)
        video = SharedVideo.objects.last()

        assert_false(video.completed)

    @istest
    def videos_are_not_approved_by_default(self):
        data = self.fake_response()
        with patch("requests.post", return_value=data):
            self.builder.create_video(self.user)
        video = SharedVideo.objects.last()

        assert_false(video.is_approved)
