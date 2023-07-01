from rest_framework.views import exception_handler
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound


def custom_exception_handler(exc, context):
    if isinstance(exc, ObjectDoesNotExist):
        exc = NotFound('Record not found')

    response = exception_handler(exc, context)

    if response is not None:
        response.data['message'] = response.data.pop('detail', '')

    return response
