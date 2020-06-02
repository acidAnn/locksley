from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Corpus(models.Model):
    title = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return f'{self.title}'


class RelationType(models.Model):
    name = models.CharField(max_length=500, unique=True)
    corpus = models.ForeignKey(Corpus, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Entity(models.Model):
    name = models.CharField(max_length=500)
    # TODO: entity type?

    def __str__(self):
        return f'{self.name}'


class Sentence(models.Model):
    text = models.CharField(max_length=500, unique=True)
    corpus = models.ForeignKey(Corpus, null=True, on_delete=models.SET_NULL)
    entities = models.ManyToManyField(Entity)

    def __str__(self):
        return f'{self.id} - {self.text}'


class Batch(models.Model):
    # TODO: add sth like a batch label
    sentences = models.ManyToManyField(Sentence,
                                       through="Membership",
                                       through_fields=('batch', 'sentence'),
                                       )
    corpus = models.ForeignKey(Corpus, null=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.id} - {self.assignee.username}'


class Membership(models.Model):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    labeled = models.BooleanField(default=False)


class Label(models.Model):
    sentence = models.ForeignKey(Sentence, null=False, on_delete=models.CASCADE)
    subject = models.ForeignKey(Entity, null=True, on_delete=models.SET_NULL, related_name="subject")
    object = models.ForeignKey(Entity, null=True, on_delete=models.SET_NULL, related_name="object")
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    relation_type = models.ForeignKey(RelationType, null=False, on_delete=models.PROTECT)

    class Meta:
        unique_together = [["sentence", "user"]]

