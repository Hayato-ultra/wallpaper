from django.conf import settings
from .models import SiteConfig


def site_config(request):
    ads_enabled = SiteConfig.objects.filter(key='ads_enabled', value='true').exists()
    return {
        'ads_enabled': ads_enabled,
        'adsense_client_id': settings.ADSENSE_CLIENT_ID,
    }
