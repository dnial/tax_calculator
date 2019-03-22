from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

from . import views

# router = routers.DefaultRouter()

app_name = "calculator"
urlpatterns = [
    url(regex=r"^user/$", view=views.User.as_view(), name="user"),
    url(regex=r"^bill/$", view=views.Bill.as_view(), name="bill"),
    url(regex=r"^bills/$", view=views.Bills.as_view(), name="bills"),
]
