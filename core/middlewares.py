import re

from rest_framework.status import is_client_error, is_success


class ResponseFormatter:
    METHOD = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

    def __init__(self, get_response):
        self.get_response = get_response
        self.API_URLS = [
            re.compile(r'^(.*)/api'),
            re.compile(r'^api'),
        ]

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_response(self, request, response):
        path = request.path_info.lstrip('/')
        valid_urls = (url.match(path) for url in self.API_URLS)

        if request.method not in self.METHOD and any(valid_urls):
            return response

        response_format = {
            'ok': is_success(response.status_code),
            'data': {},
            'message': None,
        }
        if hasattr(response, 'data') and getattr(response, 'data') is not None:
            data = response.data
            try:
                response_format['message'] = data.pop('message')
            except (KeyError, TypeError):
                response_format.update({
                    'data': data
                })
            finally:
                if is_client_error(response.status_code):
                    response_format['data'] = None
                    response_format['message'] = data
                else:
                    response_format['data'] = data
                response.data = response_format
                response.content = response.render().rendered_content
        else:
            response.data = response_format
        return response
