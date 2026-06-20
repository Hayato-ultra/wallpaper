from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.utils.html import format_html
from .models import Wallpaper, Category, Download, PageView, SiteConfig


@admin.register(Wallpaper)
class WallpaperAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'title', 'category', 'views', 'downloads', 'is_featured', 'is_published', 'created_at']
    list_filter = ['is_featured', 'is_published', 'category', 'tags']
    search_fields = ['title', 'description', 'tags']
    list_editable = ['is_featured', 'is_published']
    readonly_fields = ['cloudinary_id', 'secure_url', 'thumbnail_url', 'views', 'downloads', 'created_at', 'updated_at']
    fieldsets = [
        ('Details', {'fields': ['title', 'description', 'tags', 'category']}),
        ('Cloudinary', {'fields': ['cloudinary_id', 'secure_url', 'thumbnail_url']}),
        ('Metadata', {'fields': ['width', 'height', 'file_size', 'format', 'dominant_color']}),
        ('Stats', {'fields': ['views', 'downloads']}),
        ('Status', {'fields': ['is_featured', 'is_published', 'uploaded_by']}),
    ]

    def thumbnail_preview(self, obj):
        if obj.thumbnail_url:
            return format_html('<img src="{}" width="80" height="50" style="object-fit:contain;border-radius:4px;background:#1d1b1f" />', obj.thumbnail_url)
        return '-'
    thumbnail_preview.short_description = 'Preview'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'wallpaper_count']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ['wallpaper', 'downloaded_at']
    list_filter = ['downloaded_at']


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['wallpaper', 'viewed_at']
    list_filter = ['viewed_at']


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']
    list_editable = ['value']
