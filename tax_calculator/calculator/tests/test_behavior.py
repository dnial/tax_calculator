import pytest

from django.urls import reverse
from django.test.client import Client
from django.test.testcases import TestCase
from django.utils import timezone

from calculator.models import Codes, Items, Users
from calculator.tests import utils

pytestmark = pytest.mark.django_db


class TestUserCreation:
    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        user_name = "Timbul"
        data = {"name": user_name}

        client = Client()
        url = reverse("calculator:user")

        response = client.post(url, data=data)

        assert response.status_code == 200
        assert response.data["name"] == user_name

        user_id = response.data["id"]

        response = client.get(url, {"id": user_id})
        assert response.status_code == 200
        assert response.data["name"] == user_name


class TestBillCreation:

    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        user_name = "Tessy"
        data = {"name": user_name}

        client = Client()
        url = reverse("calculator:user")

        response = client.post(url, data=data)

        assert response.status_code == 200
        assert response.data["name"] == user_name

        user_id = response.data["id"]

        url = reverse("calculator:bill")
        bill_data = {
            "name": "Standup Comedy",
            "price": 1000,
            "user_id": user_id,
            "tax_code": 3
        }

        response = client.post(url, data=bill_data)

        assert response.status_code == 200
        assert response.data["name"] == bill_data["name"]
        assert response.data["price"] == str(bill_data["price"])
        assert response.data["user_id"] == bill_data["user_id"]
        assert response.data["user_name"] == user_name

        response = client.get(url, {"id": response.data["id"]})
        assert response.status_code == 200
        assert response.data["name"] == bill_data["name"]
        assert response.data["user_id"] == bill_data["user_id"]
        assert response.data["user_name"] == user_name


class TestBillCalculation:

    def tearDown(self):
        utils.clear_all()

    def test_positive(self):
        user_name = "Gogon"
        data = {"name": user_name}

        client = Client()
        url = reverse("calculator:user")

        response = client.post(url, data=data)

        assert response.status_code == 200
        assert response.data["name"] == user_name

        user_id = response.data["id"]

        url = reverse("calculator:bill")
        bill_data_1 = {
            "name": "Whooper XL",
            "price": 1000,
            "user_id": user_id,
            "tax_code": 1
        }

        bill_data_2 = {
            "name": "Marlboro",
            "price": 1000,
            "user_id": user_id,
            "tax_code": 2
        }

        bill_data_3 = {
            "name": "Karaoke",
            "price": 150,
            "user_id": user_id,
            "tax_code": 3
        }

        response = client.post(url, data=bill_data_1)
        response = client.post(url, data=bill_data_2)
        response = client.post(url, data=bill_data_3)

        url = reverse("calculator:bills")
        response = client.get(url, {"user_id": user_id})

        assert response.data["price_subtotal"] == 2150
        assert response.data["tax_subtotal"] == 220.5
        assert response.data["grand_total"] == 2370.5
