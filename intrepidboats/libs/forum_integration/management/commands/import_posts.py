import csv
from itertools import groupby
from operator import itemgetter

from intrepidboats.libs.forum_integration.exceptions import AlreadyImportedPostException
from ..utils.post_content_manupulation import update_urls_in, update_imgs_in
from intrepidboats.libs.forum_integration.models import ImportedPost
from ._base import BaseImportCommand


class Command(BaseImportCommand):
    help = 'Import old forum data'
    file_name = "post_without_messages.csv"
    EXPECTED_LEN = 15
    MARK = ",===MARK==="

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout=stdout, stderr=stderr, no_color=no_color)
        self.messages_dict = None

    def process_rows(self, rows):
        with open(self.get_file_path("post_with_messages.csv"), newline='') as csvfile:
            content = csvfile.read()
            messages = [row.strip().replace("\ufeff", "").split(",", 1) for row in content.split(self.MARK)]
            self.messages_dict = dict([(row[0], row[1]) for row in messages if all(row)])
        cmd = self

        def grouper(row):
            return cmd.get_data_from_row(row)

        groups = groupby(rows, grouper)
        for _, posts in groups:
            ordered = sorted(list(posts), key=itemgetter(1))
            for post in ordered:
                self.import_from(row=post)

    def get_reader(self, csvfile):
        return csv.reader(csvfile, delimiter=',', )

    def do_import(self, row):
        row_data = ", ".join(row)
        message_id, topic_id, position, user_id, username, posted_at = self.get_data_from_row(row)
        message = self.get_message(message_id)
        ImportedPost.objects.import_post(message_id, topic_id, user_id, username, message,
                                         posted_at, position, row_data)

    def get_data_from_row(self, row):
        return (
            row[0],  # MessageId
            row[1],  # TopicId
            row[3],  # Position
            row[5],  # UserId
            row[6],  # UserName
            row[7],  # PostedAt
        )

    def is_already_imported(self, data):
        return ImportedPost.objects.already_imported(self.get_id(data))

    def raise_already_imported(self, data):
        raise AlreadyImportedPostException(self.get_id(data))

    def get_topic_id(self, row):
        return self.get_data_from_row(row)[1]

    def get_name(self, data):
        return data[3]

    def get_message(self, message_id):
        message = self.messages_dict.get(message_id, None)
        if message is None:
            raise ValueError("No message found for ID: %s" % message_id)
        message = update_urls_in(message)
        message = update_imgs_in(message)
        return message

    def get_id(self, data):
        return data[0]
