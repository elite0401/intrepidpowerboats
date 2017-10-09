from django.contrib.auth import get_user_model
from machina.apps.forum.models import Forum
from machina.apps.forum_conversation.models import Topic, Post


class AlreadyImportedException(Exception):
    def __init__(self, model, key):
        self.model = model
        self.key = key
        super(AlreadyImportedException, self).__init__("Already imported %s with key %s" % (self.model, self.key))


class AlreadyImportedUserException(AlreadyImportedException):
    def __init__(self, email):
        self.email = email
        super(AlreadyImportedUserException, self).__init__(get_user_model().__name__, self.email)


class AlreadyImportedForumException(AlreadyImportedException):
    def __init__(self, name):
        self.name = name
        super(AlreadyImportedForumException, self).__init__(Forum.__name__, self.name)


class AlreadyImportedTopicException(AlreadyImportedException):
    def __init__(self, name):
        self.name = name
        super(AlreadyImportedTopicException, self).__init__(Topic.__name__, self.name)


class AlreadyImportedPostException(AlreadyImportedException):
    def __init__(self, message_id):
        self.message_id = message_id
        super(AlreadyImportedPostException, self).__init__(Post.__name__, self.message_id)
