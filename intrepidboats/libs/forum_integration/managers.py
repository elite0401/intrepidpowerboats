from django.contrib.auth import get_user_model
from django.db.models import Manager
from django.utils.dateparse import parse_datetime
from django.utils.text import slugify
from machina.apps.forum.models import Forum
from machina.apps.forum_conversation.models import Topic, Post
from machina.conf.settings import TOPIC_ANSWER_SUBJECT_PREFIX


class ImportedUserManager(Manager):
    def import_user(self, username, name, email, old_user_id, row_data):
        user = self.create_user(
            old_user_id,
            username,
            name,
            email,
        )
        return self.create(
            user=user,
            old_user_id=old_user_id,
            username=username,
            name=name,
            email=email,
            row_data=row_data,
        )

    def already_imported(self, user_id):
        return self.filter(old_user_id=user_id).exists()

    def create_user(self, user_id, username, name, email):
        # Sadly emails and usernames ARE NOT unique
        username = slugify(username)
        if get_user_model().objects.filter(username=username).exists():
            username = "_".join([username, user_id])
        return get_user_model().objects.create(email=email, username=username, first_name=name or username)


class ImportedForumManager(Manager):
    def already_imported(self, name):
        return self.filter(name=name).exists()

    def import_forum(self, forum_id, name, description, row_data):
        forum = self.create_forum(
            name,
            description,
        )
        return self.create(
            forum=forum,
            old_forum_id=forum_id,
            name=name,
            description=description,
            row_data=row_data,
        )

    def create_forum(self, name, description):
        return Forum.objects.create(
            name=name,
            slug=slugify(name),
            description=description,
            type=Forum.FORUM_POST
        )


class ImportedTopicManager(Manager):
    def already_imported(self, topic_id):
        return self.filter(topic_id=topic_id).exists()

    def import_topic(self, topic_id, forum_id, poster_id, name,  # pylint: disable=R0913
                     views_count, posts_count, is_deleted, row_data):
        from .models import ImportedForum, ImportedUser
        real_forum = ImportedForum.objects.get(old_forum_id=forum_id).forum
        real_poster = None
        try:
            real_poster = ImportedUser.objects.get(old_user_id=poster_id).user
        except ImportedUser.DoesNotExist:
            pass
        topic = self.create_topic(
            name,
            real_forum,
            real_poster,
            views_count,
            posts_count,
            is_deleted,
        )
        return self.create(
            topic=topic,
            old_forum_id=forum_id,
            old_topic_id=topic_id,
            old_poster_id=poster_id,
            name=name,
            views_count=views_count,
            posts_count=posts_count,
            is_deleted=is_deleted,
            row_data=row_data,
        )

    def create_topic(self, name, forum, user, views_count, posts_count, is_deleted):
        approved = True
        if is_deleted == "1":
            approved = False
        topic = Topic.objects.create(
            approved=approved,
            subject=name,
            slug=slugify(name),
            forum=forum,
            poster=user,
            views_count=views_count,
            posts_count=posts_count,
            type=Topic.TOPIC_POST,
            status=Topic.TOPIC_UNLOCKED,
        )
        Post.objects.create(
            subject=name,
            content=name,
            topic=topic,
            poster=user,
            username=user.username,
        )
        return topic


class ImportedPostManager(Manager):
    def already_imported(self, post_id):
        return self.filter(old_post_id=post_id).exists()

    def import_post(self, message_id, topic_id, user_id, username,  # pylint: disable=R0913
                    message, posted_at, position, row_data):
        from .models import ImportedUser, ImportedTopic
        real_poster = None
        try:
            real_poster = ImportedUser.objects.get(old_user_id=user_id).user
        except ImportedUser.DoesNotExist:
            pass
        try:
            real_topic = ImportedTopic.objects.get(old_topic_id=topic_id).topic
        except ImportedTopic.DoesNotExist:
            raise ValueError("Topic with ID %s does not exist" % topic_id)
        created_at = parse_datetime(posted_at)
        # Fix topic first post
        if position == "0" and real_topic.posts.count() == 1:
            post = real_topic.posts.first()
            post.content = message
        else:
            post = self.create_post(
                message,
                real_topic,
                real_poster,
                username,
                created_at
            )
        post.created = created_at
        post.save()

        return self.create(
            post=post,
            old_topic_id=topic_id,
            old_post_id=message_id,
            old_poster_id=user_id,
            old_username=username,
            old_posted_at=posted_at,
            message=message,
            row_data=row_data,
        )

    def create_post(self, message, topic, user, username, created_at):
        return Post.objects.create(
            subject='{} {}'.format(TOPIC_ANSWER_SUBJECT_PREFIX, topic.subject),
            content=message,
            poster=user,
            topic=topic,
            username=username,
            created=created_at,
        )
