import json
from django.conf import settings
from .models import SiteConfig, Category


def site_config(request):
    ads_enabled = SiteConfig.objects.filter(key='ads_enabled', value='true').exists()
    cats = list(Category.objects.values_list('name', flat=True).order_by('-wallpaper_count'))
    return {
        'ads_enabled': ads_enabled,
        'adsense_client_id': settings.ADSENSE_CLIENT_ID,
        'all_categories_json': json.dumps(cats),
        'all_categories': cats,
    }
