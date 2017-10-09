import csv
from os.path import join
import logging
import environ
from django.core.management import BaseCommand

from intrepidboats.libs.forum_integration.exceptions import AlreadyImportedException

logger = logging.getLogger(__name__)  # pylint: disable=C0103


class BaseImportCommand(BaseCommand):
    file_name = None

    def handle(self, *args, **options):
        logging.info("Start parsing file: %s", self.file_name)
        self.read_file(self.get_default_file_path())

    def read_file(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = self.get_reader(csvfile)
            rows = list(reader)[1:]
            logging.info("Processing %s rows", len(rows))
            self.process_rows(rows=rows)

    def get_default_file_path(self):
        return self.get_file_path(self.file_name)

    def get_file_path(self, a_file):
        lib_path = environ.Path(__file__) - 3
        files_path = join(str(lib_path), "files", "forum")
        return join(files_path, a_file)

    def get_reader(self, csvfile):
        return csv.reader(csvfile, delimiter=',')

    def process_rows(self, rows):
        for row in rows:
            self.import_from(row=row)

    def import_from(self, row):
        row_data = ",".join(row)
        try:
            self.validate_data(row)
            self.do_import(row)
        except ValueError as e:
            logging.error("Cannot import row with data: \n %s", row_data)
            logging.error(str(e))
        except IndexError as e:
            logging.error("Cannot import row with data: \n %s", row_data)
            logging.error(str(e))
        except AlreadyImportedException as e:
            logging.error(str(e))

    def do_import(self, row):
        raise NotImplementedError()

    def get_data_from_row(self, row):
        raise NotImplementedError()

    def is_already_imported(self, data):
        raise NotImplementedError()

    def raise_already_imported(self, data):
        raise NotImplementedError()

    def validate_data(self, row):
        row_data = ",".join(row)
        data = self.get_data_from_row(row)
        if not self.is_valid_data(data):
            raise ValueError("Invalid data %s" % row_data)
        elif self.is_already_imported(data):
            self.raise_already_imported(data)

    def is_valid_data(self, data):
        return any([value.strip() for value in data])
