from django.conf import settings
from django.db import models
from django.utils import timezone


class VimeoRateLimiting(models.Model):
    """
    Stores Vimeo API rate limiting data.
    Each API call informs the caller on the remaining amount of requests allowed before Vimeo issues a temporary
    block. It also sends the time when this value will reset. (Typically, the amount of allowed requests resets after
    15 minutes without a request.)
    """
    reset_time = models.DateTimeField(verbose_name="reset time")
    remaining_requests = models.IntegerField(verbose_name="remaining requests")

    @classmethod
    def get_instance(cls):
        if cls.objects.all().exists():
            return cls.objects.first()
        else:
            return cls.objects.create(reset_time=timezone.now(), remaining_requests=500)

    def update_with(self, reset_time, remaining_requests):
        self.reset_time = reset_time
        self.remaining_requests = remaining_requests
        self.save()

    def available_for_request(self):
        """If there are too few allowed requests left, avoid calling the API until after reset time."""
        return self.remaining_requests > settings.VIMEO_API_REQUEST_LIMIT or timezone.now() >= self.reset_time
