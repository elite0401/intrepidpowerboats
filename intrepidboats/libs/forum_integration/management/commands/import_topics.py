from intrepidboats.libs.forum_integration.exceptions import AlreadyImportedTopicException
from intrepidboats.libs.forum_integration.models import ImportedTopic
from ._base import BaseImportCommand


class Command(BaseImportCommand):
    help = 'Import old forum data'
    file_name = "topics.csv"

    def do_import(self, row):
        row_data = ", ".join(row)
        topic_id, forum_id, poster_id, name, view_count, posts_count, is_deleted = self.get_data_from_row(row)
        ImportedTopic.objects.import_topic(
            topic_id, forum_id, poster_id, name,
            view_count, posts_count, is_deleted, row_data
        )

    def get_data_from_row(self, row):
        return (
            row[0],  # TopicID
            row[1],  # ForumId
            row[2],  # posterId
            row[5],  # Name
            row[6],  # ViewCount
            row[14],  # PostsCount
            row[16],  # IsDeleted
        )

    def is_already_imported(self, data):
        return ImportedTopic.objects.already_imported(self.get_id(data))

    def raise_already_imported(self, data):
        raise AlreadyImportedTopicException(self.get_name(data))

    def get_id(self, data):
        return data[0]

    def get_name(self, data):
        return data[3]
