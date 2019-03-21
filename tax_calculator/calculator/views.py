import sys
import traceback
import uuid

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        """

        data = request.GET
        user_id = data.get('id', None)
        user_data = user.get_user(user_id=user_id)
        data = {
            "id": user_data.id,
            "name": user_data.name
        }

        return JsonResponse(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        API link: /user/
        """

        data = request.data
        name = data.get("name", None)

        new_user = user.create_user(name=name)
        data = {
            "id": new_user.id,
            "name": new_user.name
        }

        return Response(data)


