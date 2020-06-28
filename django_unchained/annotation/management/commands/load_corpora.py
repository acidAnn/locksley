import json

from django.core.management.base import BaseCommand, CommandError
from annotation.models import Corpus


class Command(BaseCommand):
    help = "Load corpora."

    def handle(self, *args, **options):
        with open("/data/corpora.json", encoding="utf8") as input_file:
            corpora_list = json.load(input_file)

        before = Corpus.objects.count()

        for corpus in corpora_list:
            corpus_instance, created = Corpus.objects.get_or_create(
                title=corpus["title"],
                tag_line=corpus["tag_line"],
                description=corpus["description"],
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'"{corpus_instance}"'))
            else:
                self.stdout.write(f'"{corpus_instance}"')

        self.stdout.write(
            f"before: {before} corpora, after: {Corpus.objects.count()} corpora"
        )
