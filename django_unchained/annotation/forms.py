from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Label, RelationType, Entity, ExampleEntity


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'mind. 8 Zeichen, nicht nur Ziffern'


class LabelForm(forms.ModelForm):
    entity1 = forms.ModelChoiceField(label="Entität 1", queryset=Entity.objects.all())
    entity2 = forms.ModelChoiceField(label="Entität 2", queryset=Entity.objects.all())
    relation_type = forms.ModelChoiceField(label="Relation", queryset=RelationType.objects.all())

    def __init__(self, *args, **kwargs):
        sentence = kwargs.pop("sentence", None)
        super(LabelForm, self).__init__(*args, **kwargs)

        relation_types = RelationType.objects.all()
        entities = Entity.objects.all()

        if sentence:
            relation_types = relation_types.filter(corpus=sentence.corpus)
            entities = sentence.entity_set.all()

        self.fields["entity1"].queryset = entities
        self.fields["entity2"].queryset = entities
        self.fields["relation_type"].queryset = relation_types

    class Meta:
        model = Label
        fields = ["entity1", "entity2", "relation_type"]


class TestRunLabelForm(forms.ModelForm):
    entity1 = forms.ModelChoiceField(label="Entität 1", queryset=ExampleEntity.objects.all())
    entity2 = forms.ModelChoiceField(label="Entität 2", queryset=ExampleEntity.objects.all())
    relation_type = forms.ModelChoiceField(label="Relation", queryset=RelationType.objects.all())

    def __init__(self, *args, **kwargs):
        example_sentence = kwargs.pop("example_sentence", None)
        super(TestRunLabelForm, self).__init__(*args, **kwargs)

        relation_types = RelationType.objects.all()
        entities = ExampleEntity.objects.all()

        if example_sentence:
            relation_types = relation_types.filter(corpus=example_sentence.corpus)
            entities = example_sentence.exampleentity_set.all()

        self.fields["entity1"].queryset = entities
        self.fields["entity2"].queryset = entities
        self.fields["relation_type"].queryset = relation_types

    class Meta:
        model = Label
        fields = ["entity1", "entity2", "relation_type"]


LabelFormSet = forms.formset_factory(
    LabelForm,
    extra=1
)

TestRunLabelFormSet = forms.formset_factory(
    TestRunLabelForm,
    extra=1
)
