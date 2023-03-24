from rest_framework.views import exception_handler
from http import HTTPStatus


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_payload = {
            "error": {
                "status_code": 0,
                "message": [],
            }
        }
        error = error_payload["error"]
        status_code = response.status_code

        error["status_code"] = status_code
        error["message"] = response.data.get('detail')
        response.data = error_payload
    return response
