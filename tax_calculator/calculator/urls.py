from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

from . import views

# router = routers.DefaultRouter()

app_name = "calculator"
urlpatterns = [
    url(regex=r"^$", view=views.Location.as_view(), name="location"),
    url(regex=r"^updated_on/$", view=views.LastUpdate.as_view(), name="updated_on"),
    url(regex=r"^area/$", view=views.Area.as_view(), name="area"),
    url(regex=r"^area/updated_on/$", view=views.AreaLastUpdate.as_view(), name="area_updated_on"),
]
