from rest_framework import status
from rest_framework.response import Response


class CustomResponse:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def success_response(self):
        data = {
            'status_code': status.HTTP_200_OK,
            'status': True,
            'message': 'Success',
            **self.kwargs
        }
        return Response(data)

    def failed_response(self):
        data = {
            'status_code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'Failed',
            **self.kwargs
        }
        return Response(data)
