"""Module for loading a batch from a json file and saving it in as Batch object in the database.

Classes:
Command
"""

import json

from annotation.models import Corpus, Batch, Sentence, Membership
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """A command for loading Batch objects into the database."""

    help = "Load batches."

    def handle(self, *args, **options):
        before = Batch.objects.count()

        for i in range(2):
            # for double annotation, the users are divided into two groups ("0" and "1")
            # batches belong either to group "0" or group "1"
            self.stdout.write(f"Load batches for group {i}")

            with open(f"/data/batches_group{i}.json", encoding="utf8") as input_file:
                batch_list = json.load(input_file)

            for batch in batch_list:
                try:
                    corpus = Corpus.objects.get(title=batch["corpus"])

                    batch_instance = Batch(corpus=corpus, group=batch["group"])
                    batch_instance.save()

                    self.stdout.write(self.style.SUCCESS(f'"{batch_instance}"'))

                    for sentence_id in batch["sentences"]:
                        try:
                            sent = Sentence.objects.get(id=sentence_id)
                            membership_instance = Membership(
                                sentence=sent, batch=batch_instance
                            )
                            membership_instance.save()

                        except ObjectDoesNotExist:
                            self.stdout.write(
                                self.style.ERROR(
                                    f"no sentence with id {sentence_id} found"
                                )
                            )

                except ObjectDoesNotExist:
                    self.stdout.write(self.style.ERROR(f"no corpus {batch['corpus']} found"))

        self.stdout.write(
            f"before: {before} batches, after: {Batch.objects.count()} batches"
        )
