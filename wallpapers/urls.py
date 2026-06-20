from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('wallpaper/<uuid:pk>/', views.wallpaper_detail, name='wallpaper_detail'),
    path('wallpaper/<uuid:pk>/download/', views.wallpaper_download, name='wallpaper_download'),
    path('search/', views.search, name='search'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path('upload/', views.upload_wallpaper, name='upload_wallpaper'),
    path('api/check-hash/', views.check_wallpaper_hash, name='check_wallpaper_hash'),
    path('api/wallpapers/', views.api_wallpapers, name='api_wallpapers'),
    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/wallpapers/', views.admin_wallpapers_list, name='admin_wallpapers_list'),
    path('admin/wallpapers/<uuid:pk>/toggle-feature/', views.admin_wallpaper_toggle_feature, name='admin_wallpaper_toggle_feature'),
    path('admin/wallpapers/<uuid:pk>/toggle-publish/', views.admin_wallpaper_toggle_publish, name='admin_wallpaper_toggle_publish'),
    path('admin/wallpapers/<uuid:pk>/delete/', views.admin_wallpaper_delete, name='admin_wallpaper_delete'),
    path('admin/categories/', views.admin_categories, name='admin_categories'),
    path('admin/tags/', views.admin_tags, name='admin_tags'),
    path('admin/toggle-ads/', views.admin_toggle_ads, name='admin_toggle_ads'),
    path('admin/users/', views.admin_users, name='admin_users'),
]
