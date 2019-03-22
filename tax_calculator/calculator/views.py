import sys
import traceback
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.forms.models import model_to_dict

from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from calculator.services import user, bill, item


class User(APIView):

    def get(self, request):
        """
        API link: /user/?id=<user_id>
        Response Json:
        {
            "id": <int>
            "name": <string>
        }

        """

        data = request.GET
        user_id = data.get('id', None)
        try:
            user_data = user.get_user(user_id=user_id)
        except ObjectDoesNotExist:
            error = {"message": "User Id {} Not Found".format(user_id)}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            error = {"message": "Internal Server Error"}
            return Response(data=error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        data = {
            "id": user_data.id,
            "name": user_data.name
        }

        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        API link: /user/
        Request Json:
        {
            "name": <string>
        }

        Response Json:
        {
            "id": <int>
            "name": <string>
        }
        """

        data = request.data
        name = data.get("name", None)

        try:
            new_user = user.create_user(name=name)
        except Exception as ex:
            error = {"message": "Internal Server Error"}
            return Response(data=error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = {
            "id": new_user.id,
            "name": new_user.name
        }

        return Response(data)


class Bill(APIView):

    def get(self, request):
        """
        API link: /bill/?id=<item_id>
        Response Json:
        {
            "id": <int>
            "user_id": <int>,
            "tax_code": <int>,
            "name": <string>,
            "price": <decimal>
        }

        """

        data = request.GET
        item_id = data.get('id', None)

        try:
            item_data = item.get_items_by_id(item_id=item_id)
        except ObjectDoesNotExist:
            error = {"message": "Bill with Id {} Not Found".format(item_id)}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            error = {"message": "Internal Server Error"}
            return Response(data=error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        data = {
            "id": item_data.id,
            "code": item_data.code.id,
            "type": item_data.code.name,
            "name": item_data.name,
            "price": item_data.price,
            "user_id": item_data.user.id,
            "user_name": item_data.user.name
        }

        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        API link: /bill/
        Request json:
        {
            "user_id": <int>,
            "tax_code": <int>,
            "name": <string>,
            "price": <decimal>
        }
        """

        data = request.data
        try:
            item_data = item.create_item(data)
        except ObjectDoesNotExist as oe:
            error = {"message": str(oe)}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            error = {"message": "Internal Server Error"}
            return Response(data=error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = {
            "id": item_data.id,
            "code": item_data.code.id,
            "type": item_data.code.name,
            "name": item_data.name,
            "price": item_data.price,
            "user_id": item_data.user.id,
            "user_name": item_data.user.name
        }

        return Response(data)


class Bills(APIView):

    def get(self, request):
        """
        API link: /bills/?user_id=<user_id>
        """

        data = request.GET
        user_id = data.get('user_id', None)

        try:
            data = bill.calculate_bills(user_id=user_id)
        except ObjectDoesNotExist as oe:
            error = {"message": str(oe)}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            error = {"message": "Internal Server Error"}
            return Response(data=error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=data, status=status.HTTP_200_OK)
