import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from annotation.models import Corpus, Batch, Sentence, Entity, Membership


class Command(BaseCommand):
    help = "Load batches."

    def handle(self, *args, **options):
        with open("/data/batches.json", encoding="utf8") as input_file:
            batch_list = json.load(input_file)

        before = Batch.objects.count()

        for batch in batch_list:
            try:
                corpus = Corpus.objects.get(title=batch["corpus"])

                batch_instance = Batch(
                    corpus=corpus
                )
                batch_instance.save()

                self.stdout.write(self.style.SUCCESS(f'"{batch_instance}"'))

                for sentence in batch["sentences"]:
                    sentence_instance, sentence_created = Sentence.objects.get_or_create(
                        text=sentence["text"],
                        corpus=corpus
                    )

                    if sentence_created:
                        self.stdout.write(self.style.SUCCESS(f'"{sentence_instance}"'))
                    else:
                        self.stdout.write(f'"{sentence_instance}"')

                    membership_instance = Membership(
                        sentence=sentence_instance,
                        batch=batch_instance
                    )
                    membership_instance.save()

                    for entity in sentence["entities"]:
                        entity_instance = Entity(id=entity["id"], name=entity["name"], type=entity["type"], sentence=sentence_instance)
                        entity_instance.save()

            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(f"no corpus {corpus} found"))

        self.stdout.write(
            f"before: {before} batches, after: {Batch.objects.count()} batches"
        )