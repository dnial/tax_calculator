from django.core.exceptions import ObjectDoesNotExist

from calculator.services import user as user_services
from calculator.models import Codes, Items, Users


def create_item(data=None):
    user_id = data.get("user_id", None)
    name = data.get("name", None)
    code = data.get("tax_code", None)
    price = data.get("price", None)

    try:
        code = Codes.objects.get(id=code)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("Tax Code {} not found".format(code))

    try:
        user = user_services.get_user(user_id=user_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("User Id {} not found".format(user_id))

    item = Items(code=code, user=user, name=name, price=price)
    item.save()
    return item


def get_items_by_user(user=None):
    items = Items.objects.filter(user=user)
    return items


def get_items_by_id(item_id=None):
    item = Items.objects.get(id=item_id)
    return item
