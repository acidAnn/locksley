import json

from django.core.management.base import BaseCommand
from annotation.models import RelationType


class Command(BaseCommand):
    help = "Export relation types."

    def handle(self, *args, **options):
        relation_type_count = RelationType.objects.count()

        relation_type_list = []

        for relation_type in RelationType.objects.all():
            relation_type_list.append({
                "id": relation_type.id,
                "name": relation_type.name
            })

        with open("/data/exported_relation_types.json", mode="w", encoding="utf8") as f:
            json.dump(relation_type_list, f, ensure_ascii=False, indent=2)

        self.stdout.write(
            f"{relation_type_count} relation types exported"
        )