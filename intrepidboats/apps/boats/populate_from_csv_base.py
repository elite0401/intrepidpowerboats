import csv
import os
from os.path import join, basename, splitext

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from intrepidboats.apps.boats.models import Boat


class AbstractCsvImportCommand(BaseCommand):
    csv_dir = "CSVs"
    thumbnails_dir = "Thumbnails"

    def add_arguments(self, parser):
        parser.add_argument('dir')

    def handle(self, *args, **options):
        current_dir = os.getcwd()
        directory = options['dir']
        print(current_dir, directory)
        full_path = join(current_dir, directory)
        csv_dir = join(full_path, self.csv_dir)
        for filename in os.listdir(csv_dir):
            self.import_from_csv(filename, csv_dir, full_path)

    def import_from_csv(self, filename, csv_dir, full_path):
        boat = None
        boat_name = " ".join(splitext(filename)[0].split("_"))
        self.stdout.write(self.style.NOTICE("Processing file '%s'" % filename))
        try:
            boat = Boat.objects.get(title=boat_name)
            self.stdout.write(self.style.NOTICE("Found boat with name '%s'" % boat_name))
        except Boat.DoesNotExist as e:
            self.stdout.write(self.style.ERROR("Boat with name '%s' not found" % boat_name))
            raise e
        if boat is None:
            return
        with open(join(csv_dir, filename), newline='') as csvfile:
            items = csv.reader(csvfile)
            next(items)
            for row in items:
                self.process_item(boat, row, full_path)

    @staticmethod
    def none_to_empty_string(string):
        return string.replace('null', '').replace('NULL', '').strip()

    def process_item(self, boat, row, full_path):
        raise NotImplementedError('To be implemented in subclass')

    def get_image(self, file_path):
        content = None
        with open(file_path, "rb") as an_image:
            content = ContentFile(an_image.read(), basename(file_path))
        return content
