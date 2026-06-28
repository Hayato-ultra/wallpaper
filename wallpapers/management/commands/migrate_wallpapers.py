import sqlite3
import os
from django.core.management.base import BaseCommand
from wallpapers.models import Wallpaper


class Command(BaseCommand):
    help = 'Migrate wallpapers from local SQLite to current database'

    def add_arguments(self, parser):
        parser.add_argument('--sqlite-path', type=str, default='db.sqlite3')

    def handle(self, *args, **options):
        sqlite_path = options['sqlite_path']
        if not os.path.exists(sqlite_path):
            self.stderr.write(f'SQLite file not found: {sqlite_path}')
            return

        conn = sqlite3.connect(sqlite_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM wallpapers_wallpaper')
        rows = cursor.fetchall()
        conn.close()

        self.stdout.write(f'Found {len(rows)} wallpapers in SQLite')

        created = 0
        skipped = 0
        for row in rows:
            data = dict(row)
            sha256 = data.get('sha256', '')
            if Wallpaper.objects.filter(sha256=sha256).exists():
                skipped += 1
                continue
            Wallpaper.objects.create(
                id=data['id'],
                title=data['title'],
                description=data['description'],
                cloudinary_id=data['cloudinary_id'],
                secure_url=data['secure_url'],
                thumbnail_url=data['thumbnail_url'],
                tags=data['tags'],
                category=data['category'],
                width=data['width'],
                height=data['height'],
                file_size=data['file_size'],
                format=data['format'],
                dominant_color=data['dominant_color'],
                downloads=data['downloads'],
                views=data['views'],
                is_featured=data['is_featured'],
                is_published=data['is_published'],
                created_at=data['created_at'],
                updated_at=data['updated_at'],
                sha256=sha256,
            )
            created += 1
            if created % 50 == 0:
                self.stdout.write(f'  Imported {created}...')

        self.stdout.write(self.style.SUCCESS(f'Done: {created} created, {skipped} skipped'))
