import pytest

from calculator.services import item, user, bill
from calculator.models import Codes, Items, Users

pytestmark = pytest.mark.django_db


class TestUserCreation:
    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        # Act
        name = 'Jojon'
        j_user = user.create_user(name)

        # Assert
        assert j_user.name == name
        user_db = Users.objects.get(name=name)
        assert user_db.name == name


class TestItemCreation:
    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        # Arrange
        username = 'Tarsan'
        user = Users(name=username)
        user.save()

        price = 120000
        code = 3
        item_name = 'Football Game'
        data = {
            "name": item_name,
            "price": price,
            "user_id": user.id,
            "tax_code": code,
        }

        # Act
        itm = item.create_item(data=data)

        # Assert
        assert itm.name == item_name
        assert itm.user.name == username

        item_db = Items.objects.get(id=itm.id)
        assert item_db.name == item_name
        assert item_db.user.name == username


class TestCalculateTax:
    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        # Arrange
        b_user = Users(name='Basuki')
        b_user.save()
        assert b_user.name == 'Basuki'

        code_food = Codes.objects.get(id=1)
        assert code_food.name == 'Food & Beverage'

        code_tob = Codes.objects.get(id=2)
        assert code_tob.name == 'Tobacco'

        code_ent = Codes.objects.get(id=3)
        assert code_ent.name == 'Entertainment'

        # Act
        item_big_mac = Items(code=code_food, user=b_user, name='Big Mac', price=1000)
        item_big_mac.save()
        tax_big_mac, amount_big_mac = bill.calculate_tax(item_big_mac)

        # Assert
        assert tax_big_mac == 100
        assert amount_big_mac == 1100

        # Act
        item_lucky = Items(code=code_tob, user=b_user, name='Lucky Strike', price=1000)
        item_lucky.save()
        tax_lucky, amount_lucky = bill.calculate_tax(item_lucky)

        # Assert
        assert tax_lucky == 120
        assert amount_lucky == 1120

        # Act
        item_movie = Items(code=code_ent, user=b_user, name='Movie', price=150)
        item_movie.save()
        tax_movie, amount_movie = bill.calculate_tax(item_movie)
        
        # Assert
        assert tax_movie == 0.5
        assert amount_movie == 150.5


class TestCalculateBills:
    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        # Arrange
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

        # Act
        data = bill.calculate_bills(user_id=user.id)

        # Assert
        assert data["price_subtotal"] == 2150
        assert data["tax_subtotal"] == 220.5
        assert data["grand_total"] == 2370.5
