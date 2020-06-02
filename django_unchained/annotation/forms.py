from django.forms import ModelForm, ModelChoiceField
from .models import Label, RelationType


class LabelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        sentence = kwargs.pop('sentence', None)
        super(LabelForm, self).__init__(*args, **kwargs)

        queryset = RelationType.objects.all()
        if sentence:
            queryset = queryset.filter(corpus=sentence.corpus)
            print("OBACHT", sentence.corpus)
            print(queryset.all())

        self.fields['relation_type'] = ModelChoiceField(queryset=queryset, empty_label=None,
                                     to_field_name="name")

    class Meta:
        model = Label
        fields = ['relation_type']
