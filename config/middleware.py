import json
from django.conf import settings
from django.http import HttpResponseBase


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not hasattr(settings, 'CSP_DEFAULT_SRC'):
            return response
        if not isinstance(response, HttpResponseBase):
            return response

        directives = []
        for directive in ['DEFAULT_SRC', 'SCRIPT_SRC', 'STYLE_SRC', 'FONT_SRC', 'IMG_SRC', 'CONNECT_SRC', 'FRAME_SRC']:
            value = getattr(settings, f'CSP_{directive}', None)
            if value:
                css_name = directive.lower().replace('_', '-')
                directives.append(f"{css_name} {' '.join(value)}")

        if directives:
            response['Content-Security-Policy'] = '; '.join(directives)

        return response
