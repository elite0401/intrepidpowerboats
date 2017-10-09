from os.path import join

from environ import environ

from intrepidboats.apps.boats.models import BoatGeneralFeature, BoatGeneralFeatureItem
from intrepidboats.apps.boats.populate_from_csv_base import AbstractCsvImportCommand


class Command(AbstractCsvImportCommand):
    """
    Expects a directory relative to intrepidboats outer folder with two directories inside: 'CSVs' and 'Thumbnails'.

    The CSV file's name must be exactly the same as the title of a Boat object, except for it having '_' instead of ' '.
    The CSV file's first line will be ignored and the rest of them will have the following format:
         general_feature_title, description, image_name, vimeo_id
    which are, respectively: the title of the group of features, the name of the feature, the name of the thumbnail file
    inside the Thumbnails directory, and the id of the corresponding video.
    The last two ones are optional: if you want to have those fields empty put 'null', 'NULL', any number of spaces or
    an empty string.

    WARNING:
        If you run through the same CSVs twice you're going to get duplicates

    EXAMPLE FILE:
        general_feature_title, description, image_name, vimeo_id
        New section, This one doesn't have anything, NULL, null
        New section, This one has an image, fb-button.png,
        New section, This one has video,   , 220034891
        Another new section, This one doesn't have anything either, null, null
    """

    help = "Populate boat model's features"

    @staticmethod
    def none_to_empty_string(string):
        return string.replace('null', '').replace('NULL', '').strip()

    def process_item(self, boat, row, full_path):
        general_feature_title, description, image_name, vimeo_id = row
        image_name = self.none_to_empty_string(image_name)
        vimeo_id = self.none_to_empty_string(vimeo_id)
        message = "Processing feature item '%s'" % description
        self.stdout.write(self.style.NOTICE(message))
        if image_name:
            image_path = join(full_path, self.thumbnails_dir, image_name)
            content_file = self.get_image(image_path)
        else:
            content_file = None
        general_feature = BoatGeneralFeature.objects.get_or_create(title=general_feature_title, boat=boat)[0]
        BoatGeneralFeatureItem.objects.create(boat_general_feature=general_feature, description=description,
                                              thumbnail=content_file, vimeo_id=vimeo_id)
        self.stdout.write(self.style.SUCCESS("Processed feature item '%s'" % description))
