from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from django_select2.fields import Select2ChoiceField
from django_select2.widgets import AutoHeavySelect2Widget, Select2Widget
from .models import Animal, Service, PregnancyCheck
from .fields import BullField, CowField, ColorField, BreedField


class AnimalForm(forms.ModelForm):
    breed = BreedField(widget=AutoHeavySelect2Widget(select2_options={'minimumInputLength': 0}))
    gender = Select2ChoiceField(choices=Animal.GENDER_CHOICES, widget=Select2Widget(select2_options={'minimumInputLength': 0}))
    color = ColorField(widget=AutoHeavySelect2Widget(select2_options={'minimumInputLength': 0}))
    sire = BullField(required=False, widget=AutoHeavySelect2Widget(select2_options={'minimumInputLength': 0}))
    dam = CowField(required=False, widget=AutoHeavySelect2Widget(select2_options={'minimumInputLength': 0}))
    birth_date = forms.DateField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False}))
    weaning_date = forms.DateField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False}), required=False)
    yearling_date = forms.DateField(widget=DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False}), required=False)

    def __init__(self, *args, **kwargs):
        super(AnimalForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ('group', 'sire', 'dam'):
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Animal
        fields = ('ear_tag', 'name', 'color', 'gender', 'breed', 'sire', 'dam',
                  'birth_date', 'birth_weight', 'weaning_date', 'weaning_weight', 'yearling_date',
                  'yearling_weight')


class ServiceForm(forms.ModelForm):
    sire = BullField()
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