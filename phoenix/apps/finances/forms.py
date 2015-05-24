from datetime import date
from django import forms
from django.utils.safestring import mark_safe
from django_select2.widgets import AutoHeavySelect2Widget
from bootstrap3_datetime.widgets import DateTimePicker
from phoenix.apps.animals.fields import MultipleAnimalsField
from .models import Transaction, Category
from .fields import CategoryChoicesField


class CategoryForm(forms.ModelForm):

    class Meta:
        fields = ('name',)
        model = Category


class TransactionForm(forms.ModelForm):
    category = CategoryChoicesField(help_text=mark_safe('<button id="comment-button" class="btn btn-xs btn-primary" type="button"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span> Add Category</button>'), required=False)
    date = forms.DateField(initial=date.today(), widget=DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False}), required=False)
    animals = MultipleAnimalsField(AutoHeavySelect2Widget(select2_options={'minimumInputLength': 0, 'placeholder': 'Select Animals', 'width': 'resolve'}))

    class Meta:
        model = Transaction
        exclude = ('group', 'animal')
