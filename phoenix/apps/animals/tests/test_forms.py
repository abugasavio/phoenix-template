from datetime import date
from django.test import TestCase
from animals.forms import AnimalForm
from animals.models import Animal


class AnimalFormTestCase(TestCase):
    def test_valid_form(self):
        # Only required fields are identity and gender
        form = AnimalForm({
            'ear_tag': '102M',
            'animal_id': '101',
            'gender': Animal.GENDER_CHOICES.bull,
            'birth_date': date.today(),
            'name': 'sasa'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Identity and gender are missing
        form = AnimalForm({})
        self.assertEqual(form.errors,
                         {'birth_date': [u'This field is required.'], 'gender': [u'This field is required.'], 'name': [u'This field is required.'], '__all__': [u'Some kind of identification is required'],
                          'ear_tag': [u'This field is required.']})
