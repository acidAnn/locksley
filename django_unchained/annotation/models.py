from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Sentence(models.Model):
    text = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return f'{self.id} - {self.text}'


class Batch(models.Model):
    sentences = models.ManyToManyField(Sentence)
    assignee = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.id} - {self.assignee.username}'


class Label(models.Model):
    sentence = models.ForeignKey(Sentence, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    relation_type = models.CharField(choices=[("yummy", "Leibspeise"), ("eddi", "Lieblingseditor"), ("enemy", "Todfeind"), ("other", "Keine Relation")], max_length=500)

    class Meta:
        unique_together = [["sentence", "user"]]

