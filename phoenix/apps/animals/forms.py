from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from .models import Animal, Service, PregnancyCheck
from .fields import SireField


class AnimalForm(forms.ModelForm):
    birth_date = forms.DateField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False}))
    weaning_date = forms.DateField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False}), required=False)
    yearling_date = forms.DateField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False}), required=False)

    def __init__(self, *args, **kwargs):
        super(AnimalForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ('group',):
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Animal
        fields = ('ear_tag', 'name', 'color', 'gender', 'breed', 'sire', 'dam',
                  'birth_date', 'birth_weight', 'weaning_date', 'weaning_weight', 'yearling_date',
                  'yearling_weight')

    def clean(self):
        cleaned_data = super(AnimalForm, self).clean()
        ear_tag = cleaned_data.get('ear_tag')
        name = cleaned_data.get('name')

        if not ear_tag and not name:
            raise forms.ValidationError('Some kind of identification is required')
        return cleaned_data


class ServiceForm(forms.ModelForm):
    sire = SireField()
    date = forms.DateField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': '4'}), required=False)

    class Meta:
        model = Service
        fields = ('method', 'sire', 'date', 'notes')


class PregnancyCheckForm(forms.ModelForm):
    date = forms.DateField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False}))

    class Meta:
        model = PregnancyCheck
        fields = ('result', 'check_method', 'date',)