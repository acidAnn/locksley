"""Module for registering all models in the admin interface to the database.

This allows to add, modify and delete instances of these models via the admin interface.
"""

from django.contrib import admin
from .models import (
    Corpus,
    RelationType,
    Sentence,
    Batch,
    Label,
    Entity,
    Membership,
    TestRun,
    ExampleSentence,
    ExampleEntity,
    GoldLabel
)

admin.site.register(Corpus)
admin.site.register(RelationType)
admin.site.register(Sentence)
admin.site.register(Batch)
admin.site.register(Label)
admin.site.register(Entity)
admin.site.register(Membership)
admin.site.register(TestRun)
admin.site.register(ExampleSentence)
admin.site.register(ExampleEntity)
admin.site.register(GoldLabel)
