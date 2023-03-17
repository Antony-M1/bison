import copy
from rest_framework import (
    generics, exceptions
)
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.db.utils import (
    IntegrityError
)
from .serializers import (
    authentication
)
from ..bison_utils import constants
from ..bison_utils.util import (
    get_200_and_400_response_template
)


class SignUpAPI(generics.CreateAPIView):
    serializer_class = authentication.SignUpSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        success_response, error_response = get_200_and_400_response_template()
        try:
            serializer.is_valid(raise_exception=True)
            tokens = serializer.create(user_data)
            success_response['message'] = 'Sign Up Successfully'
            return Response(success_response, status=201)
        except exceptions.NotAcceptable as ex:
            error_response['message'] = str(ex)
            return Response(error_response, status=400)
        except IntegrityError as ex:
            error_response['message'] = str(ex)
            return Response(error_response, status=400)
        except exceptions.ValidationError as ex:
            error_response['message'] = str(ex)
            return Response(error_response, status=400)
        except Exception as ex:
            return Response({'error': str(ex)}, status=500)


class LogInAPI(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        return Response('login', 200)


def test(request, *args, **kwargs):
    return HttpResponse('test', 200)
