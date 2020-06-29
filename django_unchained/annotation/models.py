from django.contrib.auth.models import User
from django.db import models


class Corpus(models.Model):
    title = models.CharField(max_length=500, unique=True)
    tag_line = models.CharField(max_length=500, unique=True)
    description = models.CharField(max_length=10000, unique=True)

    def __str__(self):
        return f"{self.title}"


class RelationType(models.Model):
    name = models.CharField(max_length=500, unique=True)
    description = models.CharField(max_length=1000, unique=True)
    example1 = models.CharField(max_length=1000, unique=True)
    example2 = models.CharField(max_length=1000, unique=True)
    example3 = models.CharField(max_length=1000, unique=True)
    example4 = models.CharField(max_length=1000, unique=True)
    example5 = models.CharField(max_length=1000, unique=True)
    corpus = models.ForeignKey(Corpus, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Sentence(models.Model):
    text = models.CharField(max_length=500, unique=True)
    corpus = models.ForeignKey(Corpus, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.id} - {self.text}"


class Entity(models.Model):
    name = models.CharField(max_length=500)
    type = models.CharField(default="", max_length=500)
    sentence = models.ForeignKey(Sentence, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Batch(models.Model):
    sentences = models.ManyToManyField(
        Sentence, through="Membership", through_fields=("batch", "sentence"),
    )
    corpus = models.ForeignKey(Corpus, null=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    number_of_sentences = models.IntegerField(default=0)
    number_of_labeled_sentences = models.IntegerField(default=0)
    percentage_labeled = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}"


class Membership(models.Model):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    labeled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sentence.text} - Batch {self.batch.id}"


class Label(models.Model):
    sentence = models.ForeignKey(Sentence, null=False, on_delete=models.CASCADE)
    entity1 = models.ForeignKey(
        Entity, null=True, on_delete=models.PROTECT, related_name="entity1"
    )
    entity2 = models.ForeignKey(
        Entity, null=True, on_delete=models.PROTECT, related_name="entity2"
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    relation_type = models.ForeignKey(
        RelationType, null=True, on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.id} - {self.sentence}"


class TestRun(models.Model):
    corpus = models.ForeignKey(Corpus, null=True, on_delete=models.SET_NULL)
    number_of_example_sentences = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}"


class ExampleSentence(models.Model):
    text = models.CharField(max_length=500, unique=True)
    testrun = models.ForeignKey(TestRun, null=True, on_delete=models.SET_NULL)
    corpus = models.ForeignKey(Corpus, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.id} - {self.text}"


class ExampleEntity(models.Model):
    name = models.CharField(max_length=500)
    type = models.CharField(default="", max_length=500)
    example_sentence = models.ForeignKey(ExampleSentence, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class GoldLabel(models.Model):
    example_sentence = models.ForeignKey(ExampleSentence, null=False, on_delete=models.CASCADE)
    goldentity1 = models.ForeignKey(
        ExampleEntity, null=True, on_delete=models.PROTECT, related_name="goldentity1"
    )
    goldentity2 = models.ForeignKey(
        ExampleEntity, null=True, on_delete=models.PROTECT, related_name="goldentity2"
    )
    goldrelation_type = models.ForeignKey(
        RelationType, null=True, on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.example_sentence.text}"

