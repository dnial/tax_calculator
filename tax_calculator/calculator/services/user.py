from calculator.models import Codes, Items, Users

def create_user(name=""):
    user = Users(name=name)
    user.save()
    return user

def get_user(user_id=None):
    user = Users.objects.get(id=user_id)
    return user

