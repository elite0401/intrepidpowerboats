from intrepidboats.libs.forum_integration.exceptions import AlreadyImportedForumException
from intrepidboats.libs.forum_integration.models import ImportedForum
from ._base import BaseImportCommand


class Command(BaseImportCommand):
    help = 'Import old forum data'
    file_name = "forum.csv"

    def do_import(self, row):
        row_data = ", ".join(row)
        forum_id, name, description = self.get_data_from_row(row)
        ImportedForum.objects.import_forum(forum_id, name, description, row_data)

    def get_data_from_row(self, row):
        return (
            row[0],  # ForumID
            row[3],  # Name
            row[4],  # Description
        )

    def is_already_imported(self, data):
        return ImportedForum.objects.already_imported(self.get_name(data))

    def raise_already_imported(self, data):
        raise AlreadyImportedForumException(self.get_name(data))

    def get_name(self, data):
        return data[1]
