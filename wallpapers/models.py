import uuid
import json
from django.db import models
from django.contrib.auth.models import User


class TagField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 1000)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', '')
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return [t.strip() for t in value.split(',') if t.strip()]

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return []
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return [t.strip() for t in str(value).split(',') if t.strip()]

    def get_prep_value(self, value):
        if isinstance(value, list):
            return json.dumps(value)
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, list):
            return json.dumps(value)
        return value


class Wallpaper(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    cloudinary_id = models.CharField(max_length=255, unique=True)
    secure_url = models.URLField(max_length=512)
    thumbnail_url = models.URLField(max_length=512)
    tags = TagField()
    category = models.CharField(max_length=100, blank=True, default='')
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    format = models.CharField(max_length=10, blank=True, default='')
    dominant_color = models.CharField(max_length=7, blank=True, default='')
    sha256 = models.CharField(max_length=64, blank=True, default='', db_index=True)
    downloads = models.BigIntegerField(default=0)
    views = models.BigIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['category'], name='idx_wallpapers_category'),
            models.Index(fields=['-created_at'], name='idx_wallpapers_created'),
        ]

    def __str__(self):
        return self.title


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    thumbnail_url = models.URLField(max_length=512, blank=True, default='')
    wallpaper_count = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Download(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallpaper = models.ForeignKey(Wallpaper, on_delete=models.CASCADE, related_name='download_records')
    user_id = models.UUIDField(null=True, blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['wallpaper']),
            models.Index(fields=['-downloaded_at']),
        ]


class SiteConfig(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'Site Config'
        verbose_name_plural = 'Site Config'

    def __str__(self):
        return self.key


class PageView(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallpaper = models.ForeignKey(Wallpaper, on_delete=models.CASCADE, related_name='view_records')
    viewed_at = models.DateTimeField(auto_now_add=True)
    ip_hash = models.CharField(max_length=64, blank=True, default='')
    referrer = models.URLField(max_length=512, blank=True, default='')

    class Meta:
        indexes = [
            models.Index(fields=['wallpaper']),
            models.Index(fields=['-viewed_at']),
        ]
