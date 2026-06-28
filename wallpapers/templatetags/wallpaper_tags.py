from django import template
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.utils.safestring import mark_safe
import base64
import os

register = template.Library()

@register.simple_tag
def inline_static(path):
    """Inline a static file's content. For CSS/JS: returns content. For fonts: returns base64 data URI."""
    full_path = find(path)
    if not full_path:
        return ''
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.woff2', '.woff', '.ttf', '.otf'):
        with open(full_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode()
        mime = {'.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.otf': 'font/otf'}.get(ext, 'font/woff2')
        return f'data:{mime};base64,{data}'
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()

@register.simple_tag
def cloudinary_url(public_id, **transforms):
    cloud_name = settings.CLOUDINARY_CLOUD_NAME
    if not cloud_name:
        return ''
    base = f'https://res.cloudinary.com/{cloud_name}/image/upload'
    if transforms:
        tx = ','.join(f'{k}_{v}' for k, v in transforms.items())
        return f'{base}/{tx}/{public_id}'
    return f'{base}/{public_id}'

@register.simple_tag
def blur_placeholder(public_id):
    return cloudinary_url(public_id, w=50, e='blur:1000', q='auto:low')

@register.simple_tag
def adsense_client_id():
    return settings.ADSENSE_CLIENT_ID


@register.filter
def format_number(num):
    if num >= 1_000_000:
        return f'{num / 1_000_000:.1f}M'
    if num >= 1_000:
        return f'{num / 1_000:.1f}K'
    return str(num)


@register.filter
def file_size_format(bytes):
    if not bytes:
        return '0 B'
    kb = bytes / 1024
    if kb < 1024:
        return f'{kb:.0f} KB'
    mb = kb / 1024
    return f'{mb:.1f} MB'
