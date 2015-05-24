from django_select2.fields import AutoModelSelect2Field
from .models import Category


class CategoryChoicesField(AutoModelSelect2Field):
        queryset = Category.objects
        search_fields = ['name__icontains', ]
