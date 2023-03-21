from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()


class CustomModelBackend(ModelBackend):
    # def authenticate(self, request, username=None, email=None, password=None,
    #                  **kwargs):
    #     UserModel = get_user_model()
    #     try:
    #         user = UserModel.objects.get(Q(username=username) | Q(email=email))
    #     except UserModel.DoesNotExist:
    #         return None
    #     else:
    #         if user.check_password(password):
    #             return user
    #     return None

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            if email is None:
                return
        try:
            if username:
                user = UserModel._default_manager.\
                    get_by_natural_key(username=username)
            if email:
                user = UserModel._default_manager.\
                    get_by_natural_key(email=email)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if (user.check_password(password) and
                self.user_can_authenticate(user)):
                return user
