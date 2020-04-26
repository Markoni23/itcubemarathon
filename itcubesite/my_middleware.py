# my_middleware.py
from django.conf import settings

# default 30 days
MAX_AGE = getattr(settings, 'CACHE_CONTROL_MAX_AGE', 2592000)

class MaxAgeMiddleware(object):
    def process_response(self, request, response):
        response['Cache-Control'] = 'max-age=%d' % MAX_AGE
        return response