"""Module for loading a relation from a json file and saving it in as RelationType object in the database.

Classes:
Command
"""

import json

from annotation.models import Corpus, RelationType
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """A command for loading RelationType objects into the database."""

    help = "Load relation types."

    def handle(self, *args, **options):
        with open("/data/relation_types.json", encoding="utf8") as input_file:
            relation_type_list = json.load(input_file)

        before = RelationType.objects.count()

        for relation_type in relation_type_list:
            try:
                corpus = Corpus.objects.get(title=relation_type["corpus"])

                relation_type_instance, created = RelationType.objects.get_or_create(
                    name=relation_type["name"],
                    description=relation_type["description"],
                    example1=relation_type["example1"],
                    example2=relation_type["example2"],
                    example3=relation_type["example3"],
                    example4=relation_type["example4"],
                    example5=relation_type["example5"],
                    corpus=corpus,
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'"{relation_type_instance}"'))
                else:
                    self.stdout.write(f'"{relation_type_instance}"')

            except ObjectDoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"no corpus {relation_type['corpus']} found")
                )
                continue

        self.stdout.write(
            f"before: {before} relation types, after: {RelationType.objects.count()} relation types"
        )
