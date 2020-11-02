"""Module for loading a test run from a json file and saving it in as TestRun object in the database.

Classes:
Command
"""

import json

from annotation.models import (
    Corpus,
    RelationType,
    TestRun,
    ExampleSentence,
    ExampleEntity,
    GoldLabel,
)
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """A command for loading TestRun objects into the database."""

    help = "Load test runs."

    def handle(self, *args, **options):
        with open("/data/testruns.json", encoding="utf8") as input_file:
            testrun_list = json.load(input_file)

        before = TestRun.objects.count()

        for testrun in testrun_list:
            try:
                corpus = Corpus.objects.get(title=testrun["corpus"])

                testrun_instance, testrun_created = TestRun.objects.get_or_create(
                    corpus=corpus
                )

                if testrun_created:
                    self.stdout.write(self.style.SUCCESS(f'"{testrun_instance}"'))
                else:
                    self.stdout.write(f'"{testrun_instance}"')

                for example_sentence in testrun["example_sentences"]:
                    (
                        example_sentence_instance,
                        example_sentence_created,
                    ) = ExampleSentence.objects.get_or_create(
                        text=example_sentence["text"],
                        testrun=testrun_instance,
                        corpus=corpus,
                    )

                    if example_sentence_created:
                        self.stdout.write(
                            self.style.SUCCESS(f'"{example_sentence_instance}"')
                        )
                    else:
                        self.stdout.write(f'"{example_sentence_instance}"')

                    for entity in example_sentence["entities"]:
                        entity_instance = ExampleEntity(
                            id=entity["id"],
                            name=entity["name"],
                            type=entity["type"],
                            example_sentence=example_sentence_instance,
                        )
                        entity_instance.save()

                    for gold_label in example_sentence["gold_labels"]:
                        if gold_label["gold_relation_type"]:
                            try:
                                gold_entity1 = ExampleEntity.objects.get(
                                    id=gold_label["gold_entity1"]
                                )
                                gold_entity2 = ExampleEntity.objects.get(
                                    id=gold_label["gold_entity2"]
                                )
                                gold_relation_type = RelationType.objects.get(
                                    name=gold_label["gold_relation_type"]
                                )

                                (
                                    gold_label_instance,
                                    gold_label_created,
                                ) = GoldLabel.objects.get_or_create(
                                    example_sentence=example_sentence_instance,
                                    gold_entity1=gold_entity1,
                                    gold_entity2=gold_entity2,
                                    gold_relation_type=gold_relation_type,
                                )

                                if gold_label_created:
                                    self.stdout.write(
                                        self.style.SUCCESS(f'"{gold_label_instance}"')
                                    )
                                else:
                                    self.stdout.write(f'"{gold_label_instance}"')

                            except ObjectDoesNotExist:
                                self.stdout.write(
                                    self.style.ERROR(
                                        f"gold entities "
                                        f"{gold_label['gold_entity1']} or {gold_label['gold_entity2']} "
                                        f"or relation type {gold_label['gold_relation_type']} does not exist"
                                    )
                                )

                        else:
                            gold_label_instance = GoldLabel(
                                example_sentence=example_sentence_instance
                            )
                            gold_label_instance.save()

            except ObjectDoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"no corpus {testrun['corpus']} found")
                )

        self.stdout.write(
            f"before: {before} test runs, after: {TestRun.objects.count()} test runs"
        )
