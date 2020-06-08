from django.forms import ModelForm, ModelChoiceField, formset_factory
from .models import Label, RelationType, Entity


class LabelForm(ModelForm):
    subject = ModelChoiceField(label="Entität 1", queryset=Entity.objects.all())
    object = ModelChoiceField(label="Entität 2", queryset=Entity.objects.all())
    relation_type = ModelChoiceField(label="Relationstyp", queryset=RelationType.objects.all())

    def __init__(self, *args, **kwargs):
        sentence = kwargs.pop("sentence", None)
        super(LabelForm, self).__init__(*args, **kwargs)

        relation_types = RelationType.objects.all()
        entities = Entity.objects.all()
        if sentence:
            relation_types = relation_types.filter(corpus=sentence.corpus)
            entities = sentence.entities.all()

        self.fields["subject"].queryset = entities
        self.fields["object"].queryset = entities
        self.fields["relation_type"].queryset = relation_types

    class Meta:
        model = Label
        fields = ["subject", "object", "relation_type"]


LabelFormSet = formset_factory(
    LabelForm,
    extra=1
)
