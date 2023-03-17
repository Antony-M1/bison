import copy
from .constants import (
    SUCCESS_RESPONSE,
    ERROR_RESPONSE
)


def get_200_and_400_response_template():
    sucess = copy.deepcopy(SUCCESS_RESPONSE)
    error = copy.deepcopy(ERROR_RESPONSE)

    return sucess, error
