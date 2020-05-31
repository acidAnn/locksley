from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Sentence, Batch, User, Label

admin.site.register(Sentence)
admin.site.register(Batch)
admin.site.register(Label)
admin.site.register(User, UserAdmin)
