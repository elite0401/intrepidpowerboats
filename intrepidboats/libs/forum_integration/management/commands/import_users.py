from intrepidboats.libs.forum_integration.exceptions import AlreadyImportedUserException
from intrepidboats.libs.forum_integration.models import ImportedUser
from ._base import BaseImportCommand


class Command(BaseImportCommand):
    help = 'Import old users data'
    file_name = "users.csv"

    def do_import(self, row):
        row_data = ",".join(row)
        user_id, name, username, email = self.get_data_from_row(row)
        ImportedUser.objects.import_user(username, name, email, user_id, row_data)

    def get_data_from_row(self, row):
        return (
            row[0],  # UserID
            row[3],  # Name
            row[4],  # Username
            row[6],  # Email
        )

    def is_valid_data(self, data):
        return super(Command, self).is_valid_data(data) and self.get_email(data) != "NULL" and self.get_username(
            data) != "NULL"

    def is_already_imported(self, data):
        return ImportedUser.objects.already_imported(self.get_id(data))

    def raise_already_imported(self, data):
        raise AlreadyImportedUserException(self.get_id(data))

    def get_email(self, data):
        return data[3]

    def get_username(self, data):
        return data[2]

    def get_id(self, data):
        return data[0]
