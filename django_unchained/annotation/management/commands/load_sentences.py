import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from annotation.models import Corpus, Sentence, Entity


class Command(BaseCommand):
    help = "Load sentences."

    def handle(self, *args, **options):
        with open(f"/data/sentences.json", encoding="utf8") as input_file:
            sentence_list = json.load(input_file)

        before = Sentence.objects.count()

        for sentence in sentence_list:
            try:
                corpus = Corpus.objects.get(title=sentence["corpus"])

                sentence_instance, sentence_created = Sentence.objects.get_or_create(
                    id=sentence["id"],
                    text=sentence["sentence"],
                    corpus=corpus
                )

                if sentence_created:
                    self.stdout.write(self.style.SUCCESS(f'"{sentence_instance}"'))
                else:
                    self.stdout.write(f'"{sentence_instance}"')

                for entity in sentence["entities"]:
                    entity_instance = Entity(name=entity["text"], type=entity["type"], sentence=sentence_instance)
                    entity_instance.save()

            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(f"no corpus {corpus} found"))

        self.stdout.write(
            f"before: {before} sentences, after: {Sentence.objects.count()} sentences"
        )