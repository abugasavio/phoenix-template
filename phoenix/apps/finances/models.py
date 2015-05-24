from django.db import models
from django.utils.translation import ugettext as _
from smartmin.models import SmartModel
from model_utils import Choices


class Category(SmartModel):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Transaction(SmartModel):

    types = Choices(('income', _('Income')), ('expense', _('Expense')))

    category = models.ForeignKey(Category, blank=True, null=True)
    date = models.DateField()
    amount = models.IntegerField()
    animals = models.ManyToManyField('animals.Animal', null=False, blank=False, related_name='animal_transaction')
    transaction_type = models.CharField(max_length=20, choices=types, default=types.income)
