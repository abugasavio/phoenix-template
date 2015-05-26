from django_select2.views import NO_ERR_RESP
from django_select2.fields import AutoSelect2MultipleField, AutoModelSelect2Field, Select2ChoiceField
from .models import Animal, Color, Breed


class MultipleAnimalsField(AutoSelect2MultipleField):
    def get_results(self, request, term, page, context):
        # Fetch all by default
        animals = Animal.objects.all()

        # If there's actually a term, filter on it
        if term.strip() != '':
            animals = animals.filter(name__icontains=term)

        res = [(animal.id, animal.name) for animal in animals]
        return (NO_ERR_RESP, False, res)  # Any error response, Has more results, options list


class BullField(AutoModelSelect2Field):
    queryset = Animal.objects.filter(gender=Animal.GENDER_CHOICES.bull)
    search_fields = ['name__icontains']
    to_field = 'name'


class CowField(AutoModelSelect2Field):
    queryset = Animal.objects.filter(gender=Animal.GENDER_CHOICES.cow)
    search_fields = ['name__icontains']
    to_field = 'name'


class ColorField(AutoModelSelect2Field):
    queryset = Color.objects
    search_fields = ['name__icontains']
    to_field = 'name'


class BreedField(AutoModelSelect2Field):
    queryset = Breed.objects
    search_fields = ['name__icontains']
    to_field = 'name'
