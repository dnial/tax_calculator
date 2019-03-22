from calculator.models import Codes, Items, Users


def create_item(data=None):
    user_id = data.get("user_id", None)
    name = data.get("name", None)
    code = data.get("tax_code", None)
    price = data.get("price", None)

    code = Codes.objects.get(id=code)
    user = Users.objects.get(id=user_id)

    item = Items(code=code, user=user, name=name, price=price)
    item.save()
    return item


def get_items_by_user(user=None):
    items = Items.objects.filter(user=user)
    return items


def get_items_by_id(item_id=None):
    item = Items.objects.get(id=item_id)
    return item
