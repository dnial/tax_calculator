import pytest

from django.urls import reverse
from django.test.client import Client
from django.test.testcases import TestCase
from django.utils import timezone

from calculator.models import Codes, Items, Users
from calculator.tests import utils

pytestmark = pytest.mark.django_db


class TestUserView:
    def tearDown(self):
        utils.clear_all()

    def test_get(self):
        user_name = "Polo"
        new_user = Users(name=user_name)
        new_user.save()

        client = Client()
        url = reverse("calculator:user")

        response = client.get(url, {"id": new_user.id})

        # print("status code", response.status_code)
        # print(response.data)
        assert response.status_code == 200
        assert response.data["name"] == user_name

    def test_get_404(self):
        client = Client()
        url = reverse("calculator:user")

        response = client.get(url, {"id": 100102})

        # print("status code", response.status_code)
        # print(response.data)
        assert response.status_code == 404

    def test_post(self):
        user_name = "Timbul"
        data = {"name": user_name}

        client = Client()
        url = reverse("calculator:user")

        response = client.post(url, data=data)

        assert response.status_code == 200
        assert response.data["name"] == user_name

        user_id = response.data["id"]

        user_db = Users.objects.get(id=user_id)
        assert user_db.name == user_name
