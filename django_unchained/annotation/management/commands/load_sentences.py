from django.core.management.base import BaseCommand, CommandError
from annotation.models import Sentence


class Command(BaseCommand):
    help = "Load sentence."

    def add_arguments(self, parser):
        parser.add_argument("path", type=str)

    def handle(self, *args, **options):
        path = options["path"]

        with open(path) as input_file:
            sentence_list = input_file.readlines()

        before = Sentence.objects.count()

        for sentence in sentence_list:
            sentence_instance, created = Sentence.objects.get_or_create(text=sentence)

            if created:
                self.stdout.write(self.style.SUCCESS(f'"{sentence_instance}"'))
            else:
                self.stdout.write(f'"{sentence_instance}"')

        self.stdout.write(
            f"before: {before} sentences, after: {Sentence.objects.count()} sentences"
        )
