import hashlib
from apps.user.models import User
from django.utils.encoding import force_bytes


class Backend:

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return None
        if hashlib.md5(force_bytes(password)).hexdigest() == user.password:
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
