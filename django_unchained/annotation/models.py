"""Module for defining the models for the annotation data in the database.

Classes:
Corpus
RelationType
Sentence
Entity
Batch
Membership
Label
TestRun
ExampleEntity
ExampleSentence
GoldLabel
"""

from django.contrib.auth.models import User
from django.db import models


class Corpus(models.Model):
    """A model for the corpus which the sentences for annotation are drawn from.

    Its fields are
    title: str
    tag_line: str for a short summary of its properties
    description: str for a longer summary of its properties
    """
    title = models.CharField(max_length=500, unique=True)
    tag_line = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)

    def __str__(self):
        return f"{self.title}"


class RelationType(models.Model):
    """A model for a particular type of relation.

    Its fields are
    name: str
    description: str
    example1, example2, example3, example4, example5: str for 5 example sentences that express the relation
    corpus: a Corpus object that the relation is predefined for
    """
    name = models.CharField(max_length=500, unique=True)
    description = models.CharField(max_length=1000)
    example1 = models.CharField(max_length=1000)
    example2 = models.CharField(max_length=1000)
    example3 = models.CharField(max_length=1000)
    example4 = models.CharField(max_length=1000)
    example5 = models.CharField(max_length=1000)
    corpus = models.ForeignKey(Corpus, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Sentence(models.Model):
    """A model for a sentence.

    Its fields are
    text: str
    corpus: a Corpus object which the sentence is drawn from
    """
    text = models.CharField(max_length=500, unique=True)
    corpus = models.ForeignKey(Corpus, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.id} - {self.text}"


class Entity(models.Model):
    """A model for an entity mention.

    Its fields are
    name: str
    type: str for its named entity type
    sentence: the Sentence object in which the entity is mentioned
    """
    name = models.CharField(max_length=500)
    type = models.CharField(default="", max_length=500)
    sentence = models.ForeignKey(Sentence, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Batch(models.Model):
    """A model for a batch of sentences.

    Its fields are
    corpus: the Corpus object it was drawn from
    assignee: the User object it is assigned to
    group: str name for the user group in double annotation ("0" or "1")
    number_of_labeled_sentences: int batch size

    Every sentence is annotated two times. Therefore, it is also part of two batches.
    All users are divided into two groups (cf. above) and each group receives the same set of sentences.
    """
    sentences = models.ManyToManyField(
        Sentence, through="Membership", through_fields=("batch", "sentence"),
    )
    corpus = models.ForeignKey(Corpus, null=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    group = models.CharField(default="", max_length=500)
    number_of_labeled_sentences = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}"


class Membership(models.Model):
    """A model for an association between a sentence and its batch.

    Its fields are
    sentence: the Sentence object
    batch: the associated Batch object
    labeled: boolean that indicates whether the sentence has already been labeled within this batch
    """
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    labeled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sentence.text} - Batch {self.batch.id}"


class Label(models.Model):
    """A model for a labeled relation instance.

    Its fields are
    sentence: Sentence object that is labeled
    entity1: Entity object that is the head entity
    entity2: Entity object that is the tail entity
    user: User object that indicates who has authored the label
    relation_type: RelationType object that sentence expresses between entity1 and entity2
    """
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
    """A model for a test run with example sentences and sample solutions.

    Its fields are
    corpus: the Corpus object the test run belong to
    """
    corpus = models.ForeignKey(Corpus, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.id}"


class ExampleSentence(models.Model):
    """A model for an example sentence in a test run.

    Its fields are
    text: str
    testrun: the TestRun object the example sentence belongs to
    corpus: the Corpus object the example sentence was drawn from
    """
    text = models.CharField(max_length=500, unique=True)
    testrun = models.ForeignKey(TestRun, null=True, on_delete=models.SET_NULL)
    corpus = models.ForeignKey(Corpus, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.id} - {self.text}"


class ExampleEntity(models.Model):
    """A model for an entity in an example sentence.

    Its fields are
    name: str
    type: str for the named entity type
    example_sentence: the ExampleSentence object that mentions the example entity
    """
    name = models.CharField(max_length=500)
    type = models.CharField(default="", max_length=500)
    example_sentence = models.ForeignKey(ExampleSentence, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class GoldLabel(models.Model):
    """A model for a gold label, a sample solution for an example sentence in a test run.

    Its fields are
    example_sentence: ExampleSentence object the gold label annotates
    gold_entity1: ExampleEntity that is the head entity
    gold_entity2: ExampleEntity that is the tail entity
    gold_relation_type: RelationType that example_sentence expresses between gold_entity1 and gold_entity2
    """
    example_sentence = models.ForeignKey(ExampleSentence, null=False, on_delete=models.CASCADE)
    gold_entity1 = models.ForeignKey(
        ExampleEntity, null=True, on_delete=models.PROTECT, related_name="gold_entity1"
    )
    gold_entity2 = models.ForeignKey(
        ExampleEntity, null=True, on_delete=models.PROTECT, related_name="gold_entity2"
    )
    gold_relation_type = models.ForeignKey(
        RelationType, null=True, on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.example_sentence.text}"
