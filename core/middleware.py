from django.utils import translation


class RTLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = translation.get_language()

        request.is_rtl = language in ['fa', 'ar', 'he', 'ur']

        response = self.get_response(request)
        return response