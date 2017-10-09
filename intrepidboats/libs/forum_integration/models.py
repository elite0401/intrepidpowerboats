from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from machina.apps.forum.models import Forum
from machina.apps.forum_conversation.models import Topic, Post

from .managers import ImportedUserManager, ImportedForumManager, ImportedTopicManager, ImportedPostManager


class ImportedUser(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="import_user", )
    old_user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    row_data = models.TextField()

    objects = ImportedUserManager()


class ImportedForum(TimeStampedModel):
    forum = models.OneToOneField(Forum)
    old_forum_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    row_data = models.TextField()

    objects = ImportedForumManager()


class ImportedTopic(TimeStampedModel):
    topic = models.OneToOneField(Topic)
    old_forum_id = models.IntegerField()
    old_topic_id = models.IntegerField()
    old_poster_id = models.IntegerField()
    is_deleted = models.CharField(max_length=10)
    views_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    row_data = models.TextField()

    objects = ImportedTopicManager()


class ImportedPost(TimeStampedModel):
    post = models.OneToOneField(Post)
    old_topic_id = models.IntegerField()
    old_post_id = models.IntegerField()
    old_poster_id = models.IntegerField(null=True, blank=True)
    old_username = models.CharField(max_length=255, null=True, blank=True)
    old_posted_at = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    row_data = models.TextField()

    objects = ImportedPostManager()
