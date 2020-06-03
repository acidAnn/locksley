from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    wish = models.CharField(max_length=1000, default="", unique=False)


class Corpus(models.Model):
    title = models.CharField(max_length=500, unique=True)
    tag_line = models.CharField(max_length=500, unique=True)
    description = models.CharField(max_length=10000, unique=True)

    def __str__(self):
        return f"{self.title}"


class RelationType(models.Model):
    name = models.CharField(max_length=500, unique=True)
    description = models.CharField(max_length=1000, unique=True)
    example = models.CharField(max_length=1000, unique=True)
    corpus = models.ForeignKey(Corpus, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Entity(models.Model):
    name = models.CharField(max_length=500)
    # TODO: entity type?

    def __str__(self):
        return f"{self.name}"


class Sentence(models.Model):
    text = models.CharField(max_length=500, unique=True)
    corpus = models.ForeignKey(Corpus, null=True, on_delete=models.SET_NULL)
    entities = models.ManyToManyField(Entity)

    def __str__(self):
        return f"{self.id} - {self.text}"


class Batch(models.Model):
    sentences = models.ManyToManyField(
        Sentence, through="Membership", through_fields=("batch", "sentence"),
    )
    corpus = models.ForeignKey(Corpus, default="", null=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    number_of_sentences = models.IntegerField(default=0)
    number_of_labeled_sentences = models.IntegerField(default=0)
    percentage_labeled = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} - {self.corpus.title} - {self.assignee.username}"


class Membership(models.Model):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    labeled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sentence.text} - Batch {self.batch.id}"


class Label(models.Model):
    sentence = models.ForeignKey(Sentence, null=False, on_delete=models.CASCADE)
    # set to default
    subject = models.ForeignKey(
        Entity, null=False, on_delete=models.PROTECT, related_name="subject"
    )
    # set to default
    object = models.ForeignKey(
        Entity, null=False, on_delete=models.PROTECT, related_name="object"
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    relation_type = models.ForeignKey(
        RelationType, null=False, on_delete=models.PROTECT
    )
    is_gold_label = models.BooleanField(default=False)
