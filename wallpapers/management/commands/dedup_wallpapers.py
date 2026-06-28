from django.core.management.base import BaseCommand
from django.db.models import Count
from wallpapers.models import Wallpaper


class Command(BaseCommand):
    help = 'Remove duplicate wallpapers by cloudinary_id, title, or sha256'

    def handle(self, *args, **options):
        removed = 0

        # Dedup by cloudinary_id (most reliable)
        for d in Wallpaper.objects.values('cloudinary_id').annotate(count=Count('id')).filter(count__gt=1):
            wps = Wallpaper.objects.filter(cloudinary_id=d['cloudinary_id']).order_by('-views', '-downloads')
            keep = wps.first()
            count = wps.exclude(pk=keep.pk).count()
            wps.exclude(pk=keep.pk).delete()
            removed += count
            self.stdout.write(f'  cloudinary: kept "{keep.title}" pk={keep.pk}, removed {count}')

        # Dedup by title
        for d in Wallpaper.objects.values('title').annotate(count=Count('id')).filter(count__gt=1):
            wps = Wallpaper.objects.filter(title=d['title']).order_by('-views', '-downloads')
            keep = wps.first()
            count = wps.exclude(pk=keep.pk).count()
            wps.exclude(pk=keep.pk).delete()
            removed += count
            self.stdout.write(f'  title: kept "{keep.title}" pk={keep.pk}, removed {count}')

        # Dedup by sha256
        for d in Wallpaper.objects.exclude(sha256='').values('sha256').annotate(count=Count('id')).filter(count__gt=1):
            wps = Wallpaper.objects.filter(sha256=d['sha256']).order_by('-views', '-downloads')
            keep = wps.first()
            count = wps.exclude(pk=keep.pk).count()
            wps.exclude(pk=keep.pk).delete()
            removed += count
            self.stdout.write(f'  sha256: kept "{keep.title}" pk={keep.pk}, removed {count}')

        self.stdout.write(self.style.SUCCESS(f'Removed {removed} duplicate wallpapers'))
