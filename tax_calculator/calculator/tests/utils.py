from calculator.models import Codes, Items, Users

def clear_all():
    Codes.objects.all().delete()
    Items.objects.all().delete()
    Users.objects.all().delete()