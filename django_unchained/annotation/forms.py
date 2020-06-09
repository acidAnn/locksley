from django.forms import ModelForm, ModelChoiceField, formset_factory
from .models import Label, RelationType, Entity


class LabelForm(ModelForm):
    entity1 = ModelChoiceField(label="Entität 1", queryset=Entity.objects.all())
    entity2 = ModelChoiceField(label="Entität 2", queryset=Entity.objects.all())
    relation_type = ModelChoiceField(label="Relationstyp", queryset=RelationType.objects.all())

    def __init__(self, *args, **kwargs):
        sentence = kwargs.pop("sentence", None)
        super(LabelForm, self).__init__(*args, **kwargs)

        relation_types = RelationType.objects.all()
        entities = Entity.objects.all()
        if sentence:
            relation_types = relation_types.filter(corpus=sentence.corpus)
            entities = sentence.entities.all()

        self.fields["entity1"].queryset = entities
        self.fields["entity2"].queryset = entities
        self.fields["relation_type"].queryset = relation_types

    class Meta:
        model = Label
        fields = ["entity1", "entity2", "relation_type"]


LabelFormSet = formset_factory(
    LabelForm,
    extra=1
)
