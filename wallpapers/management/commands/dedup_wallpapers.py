from django.core.management.base import BaseCommand
from django.db.models import Count
from wallpapers.models import Wallpaper


class Command(BaseCommand):
    help = 'Remove duplicate wallpapers by sha256, keeping the one with most views'

    def handle(self, *args, **options):
        dupes = (
            Wallpaper.objects.exclude(sha256='')
            .values('sha256')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )
        removed = 0
        for d in dupes:
            wps = Wallpaper.objects.filter(sha256=d['sha256']).order_by('-views', '-downloads')
            keep = wps.first()
            delete_qs = wps.exclude(pk=keep.pk)
            count = delete_qs.count()
            delete_qs.delete()
            removed += count
            self.stdout.write(f'  Kept pk={keep.pk} "{keep.title}" ({keep.views} views), removed {count} dupes')
        self.stdout.write(self.style.SUCCESS(f'Removed {removed} duplicate wallpapers'))
