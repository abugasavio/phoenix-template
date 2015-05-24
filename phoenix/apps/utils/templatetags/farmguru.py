from django import template
from django_select2.fields import Select2MultipleChoiceField, Select2ChoiceField, HeavySelect2FieldBaseMixin, HeavyMultipleChoiceField, HeavySelect2MultipleChoiceField

register = template.Library()


@register.filter
def select2(form_field):
    select2s = (Select2MultipleChoiceField, Select2ChoiceField, HeavySelect2FieldBaseMixin, HeavyMultipleChoiceField, HeavySelect2MultipleChoiceField)
    if issubclass(form_field.field.__class__, select2s):
        return True
    return False