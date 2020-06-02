from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Corpus,
    RelationType,
    Sentence,
    Batch,
    User,
    Label,
    Entity,
    Membership,
)

admin.site.register(Corpus)
admin.site.register(RelationType)
admin.site.register(Sentence)
admin.site.register(Batch)
admin.site.register(Label)
admin.site.register(Entity)
admin.site.register(Membership)
admin.site.register(User, UserAdmin)
