from calculator.models import Codes, Items, Users


def create_item(user=None, name="", code=None, price=None):        
    code = Codes.objects.get(id=code)

    item = Items(code=code, user=user, name=name, price=price)
    item.save()
    return item


def get_items_by_user(user=None):        
    items = Items.objects.filter(user=user)
    return items

