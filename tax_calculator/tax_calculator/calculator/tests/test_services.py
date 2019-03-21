import pytest

from tax_calculator.calculator import services
from tax_calculator.calculator.models import Codes, Items, Users

pytestmark = pytest.mark.django_db

class TestUserCreation:
    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        name = 'Jojon'
        user = services.create_user(name)
        
        assert user.name == name

        user_db = Users.objects.get(name=name)
        assert user_db.name == name



class TestItemCreation:
    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        username = 'Tarsan'
        user = Users(name=username)
        user.save()

        price = 120000
        code = 3
        item_name = 'Football Game'
        item = services.create_item(code=code, user=user, name=item_name, price=price)

        assert item.name == item_name
        assert item.user.name == username

        item_db = Items.objects.get(id=item.id)
        assert item_db.name == item_name
        assert item_db.user.name == username


class TestCalculateTax:
    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        user = Users(name='Basuki')
        user.save()
        assert user.name == 'Basuki'

        code_food = Codes.objects.get(id=1)
        assert code_food.name == 'Food & Beverage'

        code_tob = Codes.objects.get(id=2)
        assert code_tob.name == 'Tobacco'

        code_ent = Codes.objects.get(id=3)
        assert code_ent.name == 'Entertainment'

        item_big_mac = Items(code=code_food, user=user, name='Big Mac', price=1000)
        item_big_mac.save()

        tax_big_mac, amount_big_mac = services.calculate_tax(item_big_mac)
        assert tax_big_mac == 100
        assert amount_big_mac == 1100
       
        item_lucky = Items(code=code_tob, user=user, name='Lucky Strike', price=1000)
        item_lucky.save()

        tax_lucky, amount_lucky = services.calculate_tax(item_lucky)
        assert tax_lucky == 120
        assert amount_lucky == 1120
       
        item_movie = Items(code=code_ent, user=user, name='Movie', price=150)
        item_movie.save()

        tax_movie, amount_movie = services.calculate_tax(item_movie)
        assert tax_movie == 0.5
        assert amount_movie == 150.5

class TestCalculateBills:
    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        user = Users(name='Asmuni')
        user.save()

        code_food = Codes.objects.get(id=1)
        assert code_food.name == 'Food & Beverage'

        code_tob = Codes.objects.get(id=2)
        assert code_tob.name == 'Tobacco'

        code_ent = Codes.objects.get(id=3)
        assert code_ent.name == 'Entertainment'

        item_big_mac = Items(code=code_food, user=user, name='Big Mac', price=1000)
        item_big_mac.save()
       
        item_lucky = Items(code=code_tob, user=user, name='Lucky Strike', price=1000)
        item_lucky.save()
       
        item_movie = Items(code=code_ent, user=user, name='Movie', price=150)
        item_movie.save()

        data = services.calculate_bills(user=user)
        assert data["Price Subtotal"] == 2150
        assert data["Tax Subtotal"] == 220.5
        assert data["Grand Total"] == 2370.5
