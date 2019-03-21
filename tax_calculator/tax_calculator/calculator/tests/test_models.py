import pytest

from tax_calculator.calculator.models import Codes, Items, Users
from tax_calculator.calculator.tests import utils


pytestmark = pytest.mark.django_db


class TestModelCreation:
    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        code_food = Codes.objects.get(id=1)
        assert code_food.name == 'Food & Beverage'

        code_tob = Codes.objects.get(id=2)
        assert code_tob.name == 'Tobacco'

        code_ent = Codes.objects.get(id=3)
        assert code_ent.name == 'Entertainment'

        user = Users(name='Bambang')
        user.save()
        assert user.name == 'Bambang'

        item_big_mac = Items(code=code_food, user=user, name='Big Mac', price=10000)
        item_big_mac.save()

        assert item_big_mac.code.name == 'Food & Beverage'
        assert item_big_mac.user.name == 'Bambang'


