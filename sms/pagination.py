from rest_framework import pagination
from rest_framework.response import Response
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class CustomPagination(pagination.PageNumberPagination):
    # page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    page_query_param = 'page_number'
    max_page_size = 1000  # Maximum page size

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
            },
            "data": data,
        }
        return Response(response_data)

    def get_next_link(self):
        if not self.page.has_next():
            return None

        page_number = self.page.next_page_number()
        url = self.request.build_absolute_uri()
        url = self.replace_query_param(url, self.page_query_param, page_number)
        return url

    def get_previous_link(self):
        if not self.page.has_previous():
            return None

        page_number = self.page.previous_page_number()
        url = self.request.build_absolute_uri()
        url = self.replace_query_param(url, self.page_query_param, page_number)
        return url

    def replace_query_param(self, url, param_name, param_value):
        parsed_url = urlparse(url)
        query_dict = parse_qs(parsed_url.query)
        query_dict[param_name] = [param_value]
        new_query = urlencode(query_dict, doseq=True)
        return urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                           parsed_url.params, new_query, parsed_url.fragment))

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
    
