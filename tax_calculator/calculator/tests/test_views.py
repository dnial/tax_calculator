import pytest

from django.urls import reverse
from django.test.client import Client
from django.test.testcases import TestCase
from django.utils import timezone

from calculator.models import Codes, Items, Users
from calculator import services
from calculator.tests import utils

pytestmark = pytest.mark.django_db


class TestUserView:
    def tearDown(self):
        utils.clear_all()

    def test_get(self):
        # Arrange
        user_name = "Polo"
        new_user = Users(name=user_name)
        new_user.save()

        # Act
        client = Client()
        url = reverse("calculator:user")

        response = client.get(url, {"id": new_user.id})

        # Assert
        assert response.status_code == 200
        assert response.data["name"] == user_name

    def test_get_404(self):
        # Act
        client = Client()
        url = reverse("calculator:user")

        response = client.get(url, {"id": 100102})

        # Assert
        assert response.status_code == 404

    def test_post(self):
        # Arrange
        user_name = "Timbul"
        data = {"name": user_name}

        # Act
        client = Client()
        url = reverse("calculator:user")
        response = client.post(url, data=data)
        
        # Assert
        assert response.status_code == 200
        assert response.data["name"] == user_name

        user_id = response.data["id"]

        user_db = Users.objects.get(id=user_id)
        assert user_db.name == user_name


class TestBillView:
    def tearDown(self):
        utils.clear_all()

    def test_get(self):
        # Arrange
        username = 'Gepeng'
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
        item = services.item.create_item(data=data)
        item_id = item.id

        # Act
        client = Client()
        url = reverse("calculator:bill")
        response = client.get(url, {"id": item_id})

        # Assert
        assert response.status_code == 200
        assert response.data["name"] == item_name

    def test_get_404(self):
        # Act
        client = Client()
        url = reverse("calculator:bill")
        response = client.get(url, {"id": 100102})

        # Assert
        assert response.status_code == 404

    def test_post(self):
        # Arrange
        user_name = "Djudjuk"
        user = Users(name=user_name)
        user.save()

        price = 120000
        code = 3
        item_name = 'Playing Gundu'
        data = {
            "name": item_name,
            "price": price,
            "user_id": user.id,
            "tax_code": code,
        }

        # Act
        client = Client()
        url = reverse("calculator:bill")
        response = client.post(url, data=data)

        # Assert
        assert response.status_code == 200
        assert response.data["name"] == data["name"]

        item_db = Items.objects.get(id=response.data["id"])
        assert item_db.name == data["name"]

    def test_post_user_404(self):
        # Arrange
        price = 120000
        code = 3
        item_name = 'Playing Gundu'
        data = {
            "name": item_name,
            "price": price,
            "user_id": 123,
            "tax_code": code,
        }

        # Act
        client = Client()
        url = reverse("calculator:bill")
        response = client.post(url, data=data)

        # Assert
        assert response.status_code == 404
        assert "User Id" in response.data["message"]

    def test_post_taxcode_404(self):
        # Arrange
        user_name = "Nunung"
        user = Users(name=user_name)
        user.save()

        price = 120000
        code = 3
        item_name = 'Playing Gundu'
        data = {
            "name": item_name,
            "price": price,
            "user_id": user.id,
            "tax_code": 12,
        }

        # Act
        client = Client()
        url = reverse("calculator:bill")
        response = client.post(url, data=data)

        # Assert
        assert response.status_code == 404
        assert "Tax Code" in response.data["message"]


class TestBillsView:
    def tearDown(self):
        utils.clear_all()

    def test_get(self):
        # Arrange
        user_name = "Teguh"
        user = Users(name=user_name)
        user.save()
        user_id = user.id

        bill_data_1 = {
            "name": "Pizza Mozzarella",
            "price": 1000,
            "user_id": user_id,
            "tax_code": 1
        }

        bill_data_2 = {
            "name": "Sampoerna",
            "price": 1000,
            "user_id": user_id,
            "tax_code": 2
        }

        bill_data_3 = {
            "name": "Climbing Mountain",
            "price": 150,
            "user_id": user_id,
            "tax_code": 3
        }

        _ = services.item.create_item(bill_data_1)
        _ = services.item.create_item(bill_data_2)
        _ = services.item.create_item(bill_data_3)

        # Act
        client = Client()
        url = reverse("calculator:bills")
        response = client.get(url, {"user_id": user_id})

        # Assert
        assert response.data["price_subtotal"] == 2150
        assert response.data["tax_subtotal"] == 220.5
        assert response.data["grand_total"] == 2370.5


    def test_get_empty(self):
        # Arrange
        user_name = "Leysus"
        user = Users(name=user_name)
        user.save()

        # Act
        client = Client()
        url = reverse("calculator:bills")
        response = client.get(url, {"user_id": user.id})

        # Assert
        assert response.data["price_subtotal"] == 0
        assert response.data["tax_subtotal"] == 0
        assert response.data["grand_total"] == 0


    def test_get_404(self):
        # Act
        client = Client()
        url = reverse("calculator:bills")
        response = client.get(url, {"user_id": 404})

        # Assert
        assert response.status_code == 404
        assert "User Id" in response.data["message"]
