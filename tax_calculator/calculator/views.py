import sys
import traceback
import uuid

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.forms.models import model_to_dict
from utils.fields import PhoneNumberField, EmailField

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class User(APIView):

    def get(self, request):
        """
        API link: /user/?id=<user_id>
        """

        data = request.GET
        merchant_id = data.get('id', None)
        data = entry.get_data(merchant_id=merchant_id)

        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        API link: /user/
        """

        data = request.POST
        merchant_id = data.get('id', None)
        data = entry.get_data(merchant_id=merchant_id)

