from django.forms import ModelForm, ModelChoiceField
from .models import Label, RelationType


class LabelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        sentence = kwargs.pop('sentence', None)
        super(LabelForm, self).__init__(*args, **kwargs)

        relation_types = RelationType.objects.all()
        if sentence:
            relation_types = relation_types.filter(corpus=sentence.corpus)
            entities = sentence.entities.all()

        self.fields['subject'] = ModelChoiceField(queryset=entities, empty_label=None, to_field_name="name")
        self.fields['object'] = ModelChoiceField(queryset=entities, empty_label=None, to_field_name="name")
        self.fields['relation_type'] = ModelChoiceField(queryset=relation_types, empty_label=None, to_field_name="name")

    class Meta:
        model = Label
        fields = ['relation_type']
