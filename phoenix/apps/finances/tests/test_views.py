from datetime import date
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from model_mommy import mommy
from helpers.test_helpers import create_logged_in_user
from finances.models import Transaction


class TransactionTestCae(TestCase):

    def setUp(self):
        self.laryn = mommy.make('animals.Animal', ear_tag='432')
        self.shauna = mommy.make('animals.Animal', ear_tag='302')
        self.income = mommy.make('finances.Transaction', date=date.today(), amount=2000, transaction_type=Transaction.types.income)
        self.income.animals.add(self.shauna, self.laryn)
        self.expense = mommy.make('finances.Transaction', date=date.today(), amount=2000, transaction_type=Transaction.types.expense)
        self.expense.animals.add(self.shauna, self.laryn)

    def test_creating_transaction(self):
        user = create_logged_in_user(self)
        user.user_permissions.add(Permission.objects.get(codename='transaction_create'))
        user.user_permissions.add(Permission.objects.get(codename='transaction_list'))

        post_data = {
            'date': date.today(),
            'animals': [self.shauna.id, self.laryn.id],
            'amount': 3000
        }
        #url = reverse('finances.transaction_create') + '?type=income'
        #response = self.client.post(url, post_data, follow=True)
        #self.assertContains(response, 'Your new transaction has been created')
