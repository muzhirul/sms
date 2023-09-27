from rest_framework import pagination
from rest_framework.response import Response
from urllib.parse import urlencode

class CustomPagination(pagination.PageNumberPagination):
    # page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    page_query_param = 'page_number'
    # max_page_size = 1000  # Maximum page size

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        url = self.request.build_absolute_uri()
        query_params = urlencode({
            self.page_query_param: page_number,
            self.page_size_query_param: self.page_size,
        })
        return f"{url}?{query_params}"

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        url = self.request.build_absolute_uri()
        query_params = urlencode({
            self.page_query_param: page_number,
            self.page_size_query_param: self.page_size,
        })
        return f"{url}?{query_params}"
    
    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        
        response_data = {
            "code": 200,
            "message": "Success",
            "pagination": {
                "count": self.page.paginator.count,
                "next": next_url,
                "previous": previous_url,
                # "page_size": self.page.paginator.per_page,
                # "page_number": self.page.number,
            },
            "data": data,
            
        }
        return Response(response_data)
    
class CustomLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = 10  # Number of items per page
    # max_limit = 1000  # Maximum page size
    # limit_query_param = 'page_size'
    # offset_query_param = 'page_number'

    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        response_data = {
            "code": 200,
            "message": "Success",
            "pagination": {
                "count": self.count,
                "next": next_url,
                "previous": previous_url,
            },
            "data": data,
        }
        return Response(response_data) 
    
