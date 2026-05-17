import re
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.utils.text import slugify
from .models import Wallpaper, Category


def update_category_counts():
    from django.db.models import Count
    counts = Wallpaper.objects.filter(is_published=True).values('category').annotate(
        cnt=Count('id')
    )
    Category.objects.all().update(wallpaper_count=0)
    for c in counts:
        cat_name = c['category']
        cnt = c['cnt']
        if cat_name:
            Category.objects.filter(name__iexact=cat_name).update(wallpaper_count=cnt)


@receiver(post_save, sender=Wallpaper)
def wallpaper_saved(sender, instance, **kwargs):
    cache.clear()
    cache.delete(f'wallpaper_detail_{instance.pk}')
    if instance.category:
        for cat_name in re.split(r'[,\s]+', instance.category):
            cat_name = cat_name.strip()
            if cat_name:
                Category.objects.get_or_create(
                    slug=slugify(cat_name),
                    defaults={'name': cat_name.title()},
                )
    update_category_counts()


@receiver(post_delete, sender=Wallpaper)
def wallpaper_deleted(sender, instance, **kwargs):
    cache.clear()
    cache.delete(f'wallpaper_detail_{instance.pk}')
    update_category_counts()
