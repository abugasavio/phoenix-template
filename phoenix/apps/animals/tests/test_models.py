from django.test import TestCase
from model_mommy import mommy
from animals.models import Animal


class AnimalTestCase(TestCase):
    def setUp(self):
        self.dam = mommy.make('animals.Animal', ear_tag='456', name='dam')
        self.sire = mommy.make('animals.Animal', ear_tag='123', name='sire', gender=Animal.GENDER_CHOICES.bull)

    def test_transitions(self):
        self.assertEqual('open', self.dam.state)
        self.dam.open()
        self.dam.save()
        self.assertEqual('open', self.dam.state)
        self.dam.served()
        self.dam.save()
        self.assertEqual('served', self.dam.state)
        self.dam.pregnant()
        self.dam.save()
        self.assertEqual('pregnant', self.dam.state)
        self.dam.lactating()
        self.dam.save()
        self.assertEqual('lactating', self.dam.state)
        self.dam.disposed()
        self.dam.save()
        self.assertEqual('disposed', self.dam.state)
