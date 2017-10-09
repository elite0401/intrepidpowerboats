from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = 'Import old forum and users data'

    def handle(self, *args, **options):
        call_command("import_users")
        call_command("import_forum")
        call_command("import_topics")
        call_command("import_posts")
