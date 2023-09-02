from rest_framework.response import Response
from rest_framework import status

class CustomResponse(Response):
    def __init__(self, code=status.HTTP_200_OK, message="Success", data=None, status=None,
                 template_name=None, headers=None, exception=False, content_type=None):
        content = {
            "code": code,
            "message": message,
            "data": data,
        }
        super().__init__(data=content, status=status, template_name=template_name,
                         headers=headers, exception=exception, content_type=content_type)