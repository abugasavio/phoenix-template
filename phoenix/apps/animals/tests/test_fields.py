from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from model_mommy import mommy
from animals.models import Animal
from animals.fields import MultipleAnimalsField, SireField


class AnimalFieldTestCase(TestCase):

    def setUp(self):
        self.dam = mommy.make('animals.Animal', ear_tag='456', name='dam')
        self.sire = mommy.make('animals.Animal', ear_tag='123', name='sire', gender=Animal.GENDER_CHOICES.bull)
        self.factory = RequestFactory()

    def test_multiple_animal_field(self):
        request = self.factory.get(reverse('django_select2_central_json'))
        # result looks like this: ('nil', False, [(1L, u'dam'), (2L, u'sire')])
        results = MultipleAnimalsField().get_results(request, term='', page='1', context='')
        res = [(animal.id, animal.name) for animal in Animal.objects.all()]
        self.assertEqual(res, results[2])
        # result looks like this: ('nil', False, [(1L, u'dam')])
        results = MultipleAnimalsField().get_results(request, term='d', page='1', context='')
        self.assertEqual([(1L, u'dam')], results[2])

    def test_sire_field(self):
        request = self.factory.get(reverse('django_select2_central_json'))
        # result looks like this: ('nil', False, [(4L, u'123', {})])
        results = SireField().get_results(request, term='s', page='1', context='')
        self.assertEqual((4L, u'123', {}), results[2][0])