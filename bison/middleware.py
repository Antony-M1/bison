import copy
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt import exceptions
from django.http import JsonResponse
from rest_framework import status
from app.bison_utils.util import get_401_and_500_response_template


logger = logging.getLogger(__name__)
# https://docs.djangoproject.com/en/4.0/topics/http/middleware/#:~:text=Middleware%20is%20a%20framework%20of,for%20doing%20some%20specific%20function.


class CustomMiddleware(object):
    '''
    This class only use access token because of we are using
    JWTAuthentication for token authentication
    It's only accept the access token
    '''
    response_401, response_500 = get_401_and_500_response_template()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.META.get('HTTP_AUTHORIZATION', False):
            try:
                jwt_auth = JWTAuthentication()
                user, payload = jwt_auth.authenticate(request)
                user.payload = payload
                request.custom_auth = user
            except exceptions.AuthenticationFailed as ex:
                self.response_401['message'] = str(ex.default_detail)
                response = JsonResponse(
                    self.response_401, status=status.HTTP_401_UNAUTHORIZED)
                return response
            except Exception as ex:
                self.response_500['message'] = str(ex)
                return JsonResponse(
                    self.response_500,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        print(exception)
        try:
            self.response_500['message'] = exception.msg
        except Exception as e:
            self.response_500['message'] = str(exception)
        return JsonResponse(self.response_500,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
