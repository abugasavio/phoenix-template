from django.db import models
from django.utils.translation import ugettext as _
from smartmin.models import SmartModel
from model_utils import Choices
from django_fsm import FSMField, transition


class Breed(SmartModel):
    name = models.CharField(max_length=30)


class Color(SmartModel):
    # http://www.sss-mag.com/fernhill/cowcolor.html
    name = models.CharField(max_length=50)


class Breeder(SmartModel):
    name = models.CharField(max_length=30)


class Animal(SmartModel):

    state = FSMField(default='open')

    @transition(field=state, source='*', target='open')
    def open(self):
        pass

    @transition(field=state, source='*', target='served')
    def served(self):
        pass

    @transition(field=state, source='*', target='pregnant')
    def pregnant(self):
        pass

    @transition(field=state, source='*', target='lactating')
    def lactating(self):
        pass

    @transition(field=state, source='*', target='disposed')
    def disposed(self):
        pass

    # Choices
    STATUS_CHOICES = Choices(('active', _('Active')), )
    COLOR_CHOICES = Choices(('yellow', _('Yellow')), )
    GENDER_CHOICES = Choices(('bull', _('Bull')), ('cow', _('Cow')))

    # Identification
    ear_tag = models.CharField(max_length=30, blank=False)
    name = models.CharField(max_length=30, blank=False)

    # Description
    color = models.CharField(choices=COLOR_CHOICES, max_length=20, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    breed = models.ForeignKey(Breed, null=True, blank=True)
    sire = models.ForeignKey('self', null=True, blank=True, related_name='sire_offsprings')
    dam = models.ForeignKey('self', null=True, blank=True, related_name='dam_offsprings')

    # Calfhood
    birth_date = models.DateField(null=True, blank=True)
    birth_weight = models.IntegerField(max_length=4, null=True, blank=True)
    weaning_date = models.DateField(null=True, blank=True)
    weaning_weight = models.IntegerField(max_length=4, null=True, blank=True)
    yearling_date = models.DateField(null=True, blank=True)
    yearling_weight = models.IntegerField(max_length=4, null=True, blank=True)

    # Sire details
    code = models.CharField(max_length=10, blank=True)
    breeder = models.ForeignKey(Breeder, null=True, blank=True, related_name='sires')

    def __unicode__(self):
        return self.ear_tag


class MilkProduction(SmartModel):
    # Choices
    TIME_CHOICES = Choices(('morning', _('Morning')), ('evening', _('Evening')))

    animal = models.ForeignKey(Animal, null=False, blank=False, related_name='milkproduction')
    time = models.CharField(choices=TIME_CHOICES, max_length=10, null=False, blank=False)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    butterfat_ratio = models.DecimalField(max_digits=5, decimal_places=3)


class Service(SmartModel):
    # Choices
    METHOD_CHOICES = Choices(('artificial_insemination', _('Artificial Insemination')), ('natural_service', _('Natural Service')),)

    animal = models.ForeignKey(Animal, null=False, blank=False, related_name='animal_services')
    method = models.CharField(choices=METHOD_CHOICES, max_length=30, default=METHOD_CHOICES.artificial_insemination, blank=False)
    sire = models.ForeignKey(Animal, null=False, blank=False, related_name='sire_services')
    date = models.DateField()
    notes = models.CharField(max_length=200, blank=True)


class PregnancyCheck(SmartModel):
    # Choices
    RESULT_CHOICES = Choices(('pregnant', _('Pregnant')), ('open', _('Open')),)
    CHECK_METHOD_CHOICES = Choices(('palpation', _('Palpation')), ('ultrasound', _('Ultrasound')), ('observation', _('Observation')), ('blood', _('Blood')))

    service = models.ForeignKey(Service, null=True, blank=True, related_name='pregnancy_checks')
    animal = models.ForeignKey(Animal, null=False, blank=False, related_name='pregnancy_checks')
    result = models.CharField(choices=RESULT_CHOICES, max_length=20)
    check_method = models.CharField(choices=CHECK_METHOD_CHOICES, max_length=20)
    date = models.DateField()




