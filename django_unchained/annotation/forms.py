"""Module for displaying forms and handling their input.

Classes:
SignUpForm
LabelForm
TestRunLabelForm
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Label, RelationType, Entity, ExampleEntity


class SignUpForm(UserCreationForm):
    """A form with which a user can sign up for the annotation interface.

    The fields are the username, email address, a password and a repeat field for the password.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        # password2 is the field where the user is asked to repeat password1
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # define a helptext for the password
        self.fields['password1'].help_text = 'mind. 8 Zeichen, nicht nur Ziffern'


class LabelForm(forms.ModelForm):
    """A form for providing a sentence with a relation label.

    Fields are the head entity, the tail entity and the relation.
    """
    entity1 = forms.ModelChoiceField(label="Entität 1", queryset=Entity.objects.all())
    entity2 = forms.ModelChoiceField(label="Entität 2", queryset=Entity.objects.all())
    relation_type = forms.ModelChoiceField(label="Relation", queryset=RelationType.objects.all())

    def __init__(self, *args, **kwargs):
        sentence = kwargs.pop("sentence", None)
        super(LabelForm, self).__init__(*args, **kwargs)

        relation_types = RelationType.objects.all()
        entities = Entity.objects.all()

        if sentence:
            # only display relations that are predefined for the corpus that the sentence belongs to
            relation_types = relation_types.filter(corpus=sentence.corpus)
            # only display entities that are mentioned in the sentence
            entities = sentence.entity_set.all()

        self.fields["entity1"].queryset = entities
        self.fields["entity2"].queryset = entities
        self.fields["relation_type"].queryset = relation_types

    class Meta:
        model = Label
        fields = ["entity1", "relation_type", "entity2"]


class TestRunLabelForm(forms.ModelForm):
    """A form for providing a sentence with a relation label within the test run.

    Fields are the head entity, the tail entity and the relation.
    """
    entity1 = forms.ModelChoiceField(label="Entität 1", queryset=ExampleEntity.objects.all())
    entity2 = forms.ModelChoiceField(label="Entität 2", queryset=ExampleEntity.objects.all())
    relation_type = forms.ModelChoiceField(label="Relation", queryset=RelationType.objects.all())

    def __init__(self, *args, **kwargs):
        example_sentence = kwargs.pop("example_sentence", None)
        super(TestRunLabelForm, self).__init__(*args, **kwargs)

        relation_types = RelationType.objects.all()
        entities = ExampleEntity.objects.all()

        if example_sentence:
            # only display relations that are predefined for the corpus that the sentence belongs to
            relation_types = relation_types.filter(corpus=example_sentence.corpus)
            # only display entities that are mentioned in the sentence
            entities = example_sentence.exampleentity_set.all()

        self.fields["entity1"].queryset = entities
        self.fields["entity2"].queryset = entities
        self.fields["relation_type"].queryset = relation_types

    class Meta:
        model = Label
        fields = ["entity1", "relation_type", "entity2"]


# make it possible to provide several label forms in a row
# this is necessary for being able to label a sentence with more than one relation instance
LabelFormSet = forms.formset_factory(
    LabelForm,
    extra=1
)

# make it possible to provide several label forms in a row within the test run
TestRunLabelFormSet = forms.formset_factory(
    TestRunLabelForm,
    extra=1
)
