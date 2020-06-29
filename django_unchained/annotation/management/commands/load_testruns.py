import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from annotation.models import Corpus, RelationType, TestRun, ExampleSentence, ExampleEntity, GoldLabel


class Command(BaseCommand):
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
                    example_sentence_instance, example_sentence_created = ExampleSentence.objects.get_or_create(
                        text=example_sentence["text"],
                        testrun=testrun_instance,
                        corpus=corpus
                    )

                    if example_sentence_created:
                        self.stdout.write(self.style.SUCCESS(f'"{example_sentence_instance}"'))
                    else:
                        self.stdout.write(f'"{example_sentence_instance}"')

                    for entity in example_sentence["entities"]:
                        entity_instance = ExampleEntity(id=entity["id"], name=entity["name"], type=entity["type"], example_sentence=example_sentence_instance)
                        entity_instance.save()

                    for gold_label in example_sentence["gold_labels"]:
                        if gold_label["goldrelation_type"]:
                            try:
                                goldentity1 = ExampleEntity.objects.get(id=gold_label["goldentity1"])
                                goldentity2 = ExampleEntity.objects.get(id=gold_label["goldentity2"])
                                goldrelation_type = RelationType.objects.get(name=gold_label["goldrelation_type"])

                                gold_label_instance, gold_label_created = GoldLabel.objects.get_or_create(
                                    example_sentence=example_sentence_instance,
                                    goldentity1=goldentity1,
                                    goldentity2=goldentity2,
                                    goldrelation_type=goldrelation_type,
                                )

                                if gold_label_created:
                                    self.stdout.write(self.style.SUCCESS(f'"{gold_label_instance}"'))
                                else:
                                    self.stdout.write(f'"{gold_label_instance}"')

                            except ObjectDoesNotExist:
                                self.stdout.write(self.style.ERROR(f"gold entities {goldentity1} or {goldentity2} or relation type {goldrelation_type} does not exist"))

                        else:
                            gold_label_instance = GoldLabel(example_sentence=example_sentence_instance)
                            gold_label_instance.save()
                            print("done")

            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(f"no corpus {corpus} found"))

        self.stdout.write(
            f"before: {before} test runs, after: {TestRun.objects.count()} test runs"
        )