SUCCESS_RESPONSE = {
    "status_code": 200,
    "status": "success"
}

ERROR_RESPONSE = {
    "status_code": 400,
    "status": "error"
}

CRITICAL_ERROR_RESPONSE = {
    "status_code": 500,
    "status": "error"
}

UNAUTHORIZED_RESPONSE = {
    "status_code": 401,
    "status": "error"
}

OTP_EMAIL_RESPONSE = {
    "subject": "Bison OTP",
    "message": "This is a one-time password don't share otheres\n"
}

REMOVE_FIELDS_FROM_USER_MODEL = [
    "password",
    "otp",
    "otp_time",
    "backend",
    "_state"
]