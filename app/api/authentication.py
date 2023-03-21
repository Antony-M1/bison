import copy
from django.utils import timezone
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
)
from rest_framework.exceptions import (
    NotAcceptable, ValidationError
)
from rest_framework.generics import (
    CreateAPIView, GenericAPIView
)
from rest_framework.response import Response
from django.db.utils import (
    IntegrityError
)
from app.models import (
     User
)
from .serializers.authentication import (
    SignUpSerializer, VerifyOTPSerializer, LogInSerializer
)
from ..bison_utils.util import (
    get_200_and_400_response_template, send_mail
)
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login
from app.bison_utils.constants import (
    OTP_EMAIL_RESPONSE, REMOVE_FIELDS_FROM_USER_MODEL
)


class SignUpAPI(CreateAPIView):
    serializer_class = SignUpSerializer

    @swagger_auto_schema(tags=['auth'])
    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        success_response, error_response = get_200_and_400_response_template()
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.create(user_data)
            success_response['status_code'] = HTTP_201_CREATED
            success_response['message'] = 'Sign Up Successfully'
            success_response['data'] = {'user_id': user.user_id}
            send_otp_email(user)
            return Response(success_response, status=HTTP_201_CREATED)
        except NotAcceptable as ex:
            error_response['message'] = str(ex)
            return Response(error_response, status=HTTP_400_BAD_REQUEST)
        except IntegrityError as ex:
            error_response['message'] = str(ex)
            return Response(error_response, status=HTTP_400_BAD_REQUEST)
        except ValidationError as ex:
            error_response['message'] = str(ex)
            return Response(error_response, status=HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return User.objects.all()


def send_otp_email(user):
    send_mail(
        subject=OTP_EMAIL_RESPONSE.get('subject'),
        message=OTP_EMAIL_RESPONSE.get('message') + user.otp,
        recipient_list=['antonypraveenkumarsoftsuave@gmail.com'],
    )


class LogInAPI(CreateAPIView):
    serializer_class = LogInSerializer

    @swagger_auto_schema(tags=['auth'])
    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        success_response, error_response = get_200_and_400_response_template()

        if email and password:
            user = authenticate(request, email=email,
                                password=password)
            if user is None:
                error_response['message'] = 'Invalid email or password'
                return Response(error_response, status=HTTP_400_BAD_REQUEST)
        if username and password:
            user = authenticate(request, username=username,
                                password=password)
            if user is None:
                error_response['message'] = 'Invalid username or password'
                return Response(error_response, status=HTTP_400_BAD_REQUEST)
        if not user.is_verified:
            error_response['message'] = 'User is not verified'
            error_response['data'] = {
                'is_verified': False
            }
            return Response(error_response, status=HTTP_400_BAD_REQUEST)
        if user is not None:
            login(request, user)
            success_response['message'] = 'Login successful'
            user_data = user.__dict__
            for field in REMOVE_FIELDS_FROM_USER_MODEL:
                del user_data[field]
            success_response['data'] = {
                'user': user_data,
                'token': user.tokens()
            }
            return Response(success_response,
                            status=HTTP_200_OK)


class VerifyOTPAPI(GenericAPIView):
    serializer_class = VerifyOTPSerializer

    @swagger_auto_schema(tags=['auth'])
    def patch(self, request):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        success_response, error_response = get_200_and_400_response_template()

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            error_response['message'] = 'User Not Exist Or Invalid user_id'
            return Response(error_response, status=HTTP_400_BAD_REQUEST)
        if user:
            if user.otp == otp:
                td = timezone.now() - user.otp_time
                if int(td.total_seconds() / 60) <= 5:
                    user.is_verified = True
                    user.save()
                    success_response['message'] = 'Email Verified Successfully'
                    return Response(success_response, status=HTTP_200_OK)
                else:
                    error_response['message'] = 'OTP Expired'
                    return Response(error_response,
                                    status=HTTP_400_BAD_REQUEST)
            else:
                error_response['message'] = 'Invalid OTP'
                return Response(error_response, status=HTTP_400_BAD_REQUEST)
        else:
            error_response['message'] = 'User Not Found or Invalid user_id'
            return Response(error_response, status=HTTP_400_BAD_REQUEST)
