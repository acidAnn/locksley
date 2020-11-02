"""Module for exporting all Label objects from the database into a json file.

Classes:
Command
"""

import json

from django.core.management.base import BaseCommand
from annotation.models import Label


class Command(BaseCommand):
    """A command to export all Label objects from the database."""
    help = "Export labels."

    def handle(self, *args, **options):
        label_count = Label.objects.count()

        label_list = []

        for label in Label.objects.all():
            # label.entity1 and label.entity1 can be None
            entities = {
                "entity1": {"id": "", "name": "", "type": ""},
                "entity2": {"id": "", "name": "", "type": ""},
            }

            if label.entity1:
                entities["entity1"]["id"] = label.entity1.id
                entities["entity1"]["name"] = label.entity1.name
                entities["entity1"]["type"] = label.entity1.type

            if label.entity2:
                entities["entity2"]["id"] = label.entity2.id
                entities["entity2"]["name"] = label.entity2.name
                entities["entity2"]["type"] = label.entity2.type

            # label.relation_type can be None
            if label.relation_type:
                relation_type = label.relation_type.id
            else:
                relation_type = ""

            label_list.append(
                {
                    "id": label.id,
                    "user": label.user.username,
                    "sentence": {"id": label.sentence.id, "text": label.sentence.text},
                    "entities": entities,
                    "relation_type": relation_type,
                }
            )

        with open("/data/exported_labels.json", mode="w", encoding="utf8") as f:
            json.dump(label_list, f, ensure_ascii=False, indent=2)

        self.stdout.write(f"{label_count} labels exported")
