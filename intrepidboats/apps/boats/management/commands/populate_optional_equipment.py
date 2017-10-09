from os.path import join

from environ import environ

from intrepidboats.apps.boats.models import OptionalEquipment
from intrepidboats.apps.boats.populate_from_csv_base import AbstractCsvImportCommand


class Command(AbstractCsvImportCommand):
    help = 'Populate boats optional equipments'

    csv_dir = "CSVs"
    thumbnails_dir = "Thumnails"

    def process_item(self, boat, row, full_path):
        image_name, description = row[0], row[1]
        message = "Processing equipment '%s'" % description
        self.stdout.write(self.style.NOTICE(message))
        if image_name:
            image_path = join(full_path, self.thumbnails_dir, image_name)
            content_file = self.get_image(image_path)
        else:
            content_file = None
        OptionalEquipment.objects.create(
            description=description,
            boat_model=boat,
            thumbnail=content_file,
        )
        self.stdout.write(self.style.SUCCESS("Processed equipment '%s'" % description))
