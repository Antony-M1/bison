import copy
from .constants import (
    SUCCESS_RESPONSE,
    ERROR_RESPONSE,
    CRITICAL_ERROR_RESPONSE,
    UNAUTHORIZED_RESPONSE
)


def get_200_and_400_response_template():
    sucess = copy.deepcopy(SUCCESS_RESPONSE)
    error = copy.deepcopy(ERROR_RESPONSE)

    return sucess, error


def get_401_and_500_response_template():
    error_401 = copy.deepcopy(UNAUTHORIZED_RESPONSE)
    error_500 = copy.deepcopy(CRITICAL_ERROR_RESPONSE)

    return error_401, error_500
