import uuid
import json
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.core.cache import cache
from django.contrib import messages
from django.conf import settings
from .models import Wallpaper, Category, Download, PageView, SiteConfig
from .forms import WallpaperUploadForm, ContactForm
from .utils import upload_to_cloudinary, get_thumbnail_url, file_sha256

DEVICE_PRESETS = {
    'mobile': {'max_width': 768},
    'tablet': {'min_width': 768, 'max_width': 1366},
    'desktop': {'min_width': 1366, 'max_width': 2560},
    'ultrawide': {'min_width': 2560, 'max_width': 3840},
    '4k': {'min_width': 3840},
}

RECIPE_HELPERS = {
    'mobile': 'Portrait & small screens (≤768px)',
    'tablet': 'Mid-size screens (768–1366px)',
    'desktop': 'Standard HD (1366–2560px)',
    'ultrawide': 'Ultra-wide (2560–3840px)',
    '4k': 'Ultra HD (≥3840px)',
}


def home(request):
    featured = cache.get('home_featured')
    if featured is None:
        featured = list(Wallpaper.objects.filter(is_featured=True, is_published=True).order_by('-created_at')[:16])
        cache.set('home_featured', featured, settings.WALLPAPER_CACHE_TIMEOUT)

    trending = cache.get('home_trending')
    if trending is None:
        trending = list(Wallpaper.objects.filter(is_published=True, downloads__gte=1000).order_by('-downloads', '-views')[:16])
        cache.set('home_trending', trending, settings.WALLPAPER_CACHE_TIMEOUT)

    categories = Category.objects.all().order_by('-wallpaper_count')
    return render(request, 'wallpapers/home.html', {
        'featured': featured,
        'trending': trending,
        'categories': categories,
        'total_wallpapers': Wallpaper.objects.filter(is_published=True).count(),
    })


def explore(request):
    wallpapers = Wallpaper.objects.filter(is_published=True)
    tags_param = request.GET.get('tags')
    category_param = request.GET.get('category')
    sort = request.GET.get('sort', 'newest')
    device_param = request.GET.get('device', '')

    if tags_param:
        tag_list = [t.strip() for t in tags_param.split(',') if t.strip()]
        q_filter = Q()
        for tag in tag_list:
            q_filter |= Q(tags__icontains=tag)
        wallpapers = wallpapers.filter(q_filter)

    if category_param:
        wallpapers = wallpapers.filter(category=category_param)

    if device_param and device_param in DEVICE_PRESETS:
        preset = DEVICE_PRESETS[device_param]
        if preset.get('min_width') and preset.get('max_width'):
            wallpapers = wallpapers.filter(width__gte=preset['min_width'], width__lte=preset['max_width'])
        elif preset.get('min_width'):
            wallpapers = wallpapers.filter(width__gte=preset['min_width'])
        elif preset.get('max_width'):
            wallpapers = wallpapers.filter(width__lte=preset['max_width'])

    if sort == 'popular':
        wallpapers = wallpapers.order_by('-views')
    elif sort == 'trending':
        wallpapers = wallpapers.filter(downloads__gte=1000).order_by('-downloads', '-views')
    elif sort == 'featured':
        wallpapers = wallpapers.filter(is_featured=True).order_by('-created_at')
    else:
        wallpapers = wallpapers.order_by('-created_at')

    paginator = Paginator(wallpapers, 32)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    cache_key = f'tag_counts_{settings.WALLPAPER_CACHE_TIMEOUT}'
    sorted_tags = cache.get(cache_key)
    if sorted_tags is None:
        all_wallpapers = Wallpaper.objects.filter(is_published=True)
        tag_counts = {}
        for wp in all_wallpapers.iterator():
            if wp.tags:
                if isinstance(wp.tags, list):
                    for t in wp.tags:
                        tag_counts[t] = tag_counts.get(t, 0) + 1
                elif isinstance(wp.tags, str):
                    for t in wp.tags.split(','):
                        t = t.strip().strip('[]" ').strip("'")
                        if t:
                            tag_counts[t] = tag_counts.get(t, 0) + 1
        sorted_tags = sorted(tag_counts.items(), key=lambda x: -x[1])[:50]
        cache.set(cache_key, sorted_tags, settings.WALLPAPER_CACHE_TIMEOUT)

    featured = cache.get('explore_featured')
    if featured is None:
        featured = list(Wallpaper.objects.filter(is_featured=True, is_published=True).order_by('-created_at')[:12])
        cache.set('explore_featured', featured, settings.WALLPAPER_CACHE_TIMEOUT)

    trending = cache.get('explore_trending')
    if trending is None:
        trending = list(Wallpaper.objects.filter(is_published=True, downloads__gte=1000).order_by('-downloads', '-views')[:12])
        cache.set('explore_trending', trending, settings.WALLPAPER_CACHE_TIMEOUT)

    if request.GET.get('ajax') == '1':
        return render(request, 'includes/wallpaper_grid.html', {'page_obj': page_obj, 'ajax': True})

    categories = Category.objects.all().order_by('-wallpaper_count')

    return render(request, 'wallpapers/explore.html', {
        'page_obj': page_obj,
        'tags_list': [{'tag': k, 'count': v} for k, v in sorted_tags],
        'current_tags': tags_param or '',
        'current_category': category_param or '',
        'current_sort': sort,
        'current_device': device_param,
        'device_presets': DEVICE_PRESETS,
        'device_helpers': RECIPE_HELPERS,
        'featured': featured,
        'trending': trending,
        'categories': categories,
    })


def wallpaper_detail(request, pk):
    cache_key = f'wallpaper_detail_{pk}'
    wallpaper = cache.get(cache_key)
    if wallpaper is None:
        wallpaper = get_object_or_404(Wallpaper, pk=pk, is_published=True)
        cache.set(cache_key, wallpaper, settings.WALLPAPER_CACHE_TIMEOUT)

    wallpaper.views += 1
    wallpaper.save(update_fields=['views'])
    PageView.objects.create(wallpaper=wallpaper)

    related_key = f'wallpaper_related_{pk}'
    related = cache.get(related_key)
    if related is None:
        related = Wallpaper.objects.filter(is_published=True).exclude(pk=pk).order_by('-views')[:8]
        cache.set(related_key, list(related), settings.WALLPAPER_CACHE_TIMEOUT)

    device_hint = 'mobile'
    if wallpaper.width:
        if wallpaper.width >= 3840:
            device_hint = '4k'
        elif wallpaper.width >= 2560:
            device_hint = 'ultrawide'
        elif wallpaper.width >= 1920:
            device_hint = 'desktop'
        elif wallpaper.width >= 768:
            device_hint = 'tablet'

    return render(request, 'wallpapers/detail.html', {
        'wallpaper': wallpaper,
        'related': related,
        'device_hint': device_hint,
    })


def wallpaper_download(request, pk):
    wallpaper = get_object_or_404(Wallpaper, pk=pk, is_published=True)
    wallpaper.downloads += 1
    wallpaper.save(update_fields=['downloads'])
    Download.objects.create(wallpaper=wallpaper)
    return redirect(wallpaper.secure_url)


def search(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        results = Wallpaper.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(tags__icontains=q) | Q(category__icontains=q),
            is_published=True
        ).order_by('-views')[:32]

    return render(request, 'wallpapers/search.html', {
        'query': q,
        'results': results,
    })


def category_view(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    wallpapers = Wallpaper.objects.filter(category__iexact=cat.name, is_published=True).order_by('-created_at')
    paginator = Paginator(wallpapers, 32)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.GET.get('ajax') == '1':
        return render(request, 'includes/wallpaper_grid.html', {'page_obj': page_obj, 'ajax': True})

    sidebar_categories = Category.objects.all().order_by('-wallpaper_count')

    return render(request, 'wallpapers/category.html', {
        'category': cat,
        'page_obj': page_obj,
        'sidebar_categories': sidebar_categories,
    })


def check_wallpaper_hash(request):
    h = request.GET.get('hash', '').strip().lower()
    exists = Wallpaper.objects.filter(sha256=h).exists() if h else False
    from django.http import JsonResponse
    return JsonResponse({'exists': exists})


def privacy(request):
    return render(request, 'wallpapers/privacy.html')


def terms(request):
    return render(request, 'wallpapers/terms.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            from django.core.mail import send_mail
            try:
                send_mail(
                    subject=f'Contact: {cd["subject"]}',
                    message=f'From: {cd["name"]} <{cd["email"]}>\n\n{cd["message"]}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                )
                messages.success(request, 'Message sent! We\'ll get back to you soon.')
            except Exception:
                messages.error(request, 'Failed to send message. Please try again later.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'wallpapers/contact.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    total_wallpapers = Wallpaper.objects.count()
    total_views = Wallpaper.objects.aggregate(s=Sum('views'))['s'] or 0
    total_downloads = Wallpaper.objects.aggregate(s=Sum('downloads'))['s'] or 0
    total_users = Download.objects.values('user_id').distinct().count()

    last_30 = datetime.now() - timedelta(days=30)
    daily_stats = []
    for i in range(30):
        day = (datetime.now() - timedelta(days=29 - i)).date()
        views = PageView.objects.filter(viewed_at__date=day).count()
        downloads = Download.objects.filter(downloaded_at__date=day).count()
        daily_stats.append({'date': day.isoformat(), 'views': views, 'downloads': downloads})

    top_wallpapers = Wallpaper.objects.filter(is_published=True).order_by('-views', '-downloads')[:10]

    return render(request, 'wallpapers/admin_dashboard.html', {
        'total_wallpapers': total_wallpapers,
        'total_views': total_views,
        'total_downloads': total_downloads,
        'total_users': total_users,
        'daily_stats': daily_stats,
        'top_wallpapers': top_wallpapers,
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def upload_wallpaper(request):
    if request.method == 'POST':
        form = WallpaperUploadForm(request.POST)
        files = request.FILES.getlist('file')
        if form.is_valid() and files:
            cd = form.cleaned_data
            tag_list = [t.strip().lower() for t in cd['tags'].split(',') if t.strip()]
            uploaded = 0
            errors = []

            for f in files:
                try:
                    fhash = cd.get('sha256', '')
                    if not fhash:
                        fhash = file_sha256(f)
                    if Wallpaper.objects.filter(sha256=fhash).exists():
                        errors.append(f'{f.name}: duplicate (already uploaded)')
                        continue

                    result = upload_to_cloudinary(f, tags=tag_list)
                    if hasattr(f, 'temporary_file_path') and f.temporary_file_path():
                        import os
                        try:
                            os.unlink(f.temporary_file_path())
                        except OSError:
                            pass
                except Exception as e:
                    errors.append(f'{f.name}: {e}')
                    continue

                title = cd.get('title', '') or f.name.rsplit('.', 1)[0]
                if len(files) > 1:
                    title = f'{title}-{uploaded + 1}' if cd.get('title') else f.name.rsplit('.', 1)[0]

                Wallpaper.objects.create(
                    title=title,
                    description=cd.get('description', ''),
                    cloudinary_id=result['public_id'],
                    secure_url=result['secure_url'],
                    thumbnail_url=get_thumbnail_url(result['public_id']),
                    tags=tag_list,
                    category=cd.get('category', ''),
                    width=result.get('width'),
                    height=result.get('height'),
                    file_size=result.get('bytes'),
                    format=result.get('format'),
                    is_featured=cd.get('is_featured', False),
                    sha256=fhash,
                    uploaded_by=request.user,
                )
                uploaded += 1

            for tag in tag_list:
                from django.utils.text import slugify
                Category.objects.get_or_create(
                    slug=slugify(tag),
                    defaults={'name': tag.title()},
                )

            if uploaded:
                messages.success(request, f'{uploaded} wallpaper{"s" if uploaded > 1 else ""} uploaded successfully!')
            for err in errors:
                messages.error(request, err)
            return redirect('admin_dashboard')

        if not files:
            messages.error(request, 'No file selected.')
    else:
        form = WallpaperUploadForm()

    cats = list(Category.objects.values_list('name', flat=True).order_by('name'))
    return render(request, 'wallpapers/upload.html', {'form': form, 'categories_json': mark_safe(json.dumps(cats))})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_wallpapers_list(request):
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = {
        'newest': '-created_at',
        'oldest': 'created_at',
        'views': '-views',
        'downloads': '-downloads',
        'title': 'title',
    }
    order = valid_sorts.get(sort, '-created_at')

    wallpapers = Wallpaper.objects.all().order_by(order)
    paginator = Paginator(wallpapers, 24)
    page = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'wallpapers/admin_wallpapers.html', {
        'page_obj': page,
        'current_sort': sort,
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_wallpaper_toggle_feature(request, pk):
    wp = get_object_or_404(Wallpaper, pk=pk)
    wp.is_featured = not wp.is_featured
    wp.save(update_fields=['is_featured'])
    messages.success(request, f'"{wp.title}" {"featured" if wp.is_featured else "unfeatured"}')
    return redirect('admin_wallpapers_list')


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_wallpaper_toggle_publish(request, pk):
    wp = get_object_or_404(Wallpaper, pk=pk)
    wp.is_published = not wp.is_published
    wp.save(update_fields=['is_published'])
    status = 'published' if wp.is_published else 'unpublished'
    messages.success(request, f'"{wp.title}" {status}')
    return redirect('admin_wallpapers_list')


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_wallpaper_delete(request, pk):
    wp = get_object_or_404(Wallpaper, pk=pk)
    if request.method == 'POST':
        try:
            from .utils import delete_from_cloudinary
            delete_from_cloudinary(wp.cloudinary_id)
        except Exception:
            pass
        wp.delete()
        messages.success(request, f'"{wp.title}" deleted')
        return redirect('admin_wallpapers_list')
    return render(request, 'wallpapers/admin_wallpaper_confirm_delete.html', {'wallpaper': wp})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_categories(request):
    categories = Category.objects.all().order_by('-wallpaper_count')

    if request.method == 'POST' and request.POST.get('action') == 'add':
        name = request.POST.get('name', '').strip()
        if name:
            slug = request.POST.get('slug', '').strip() or name.lower().replace(' ', '-')
            Category.objects.get_or_create(slug=slug, defaults={'name': name})
            messages.success(request, f'Category "{name}" created')

    if request.method == 'POST' and request.POST.get('action') == 'delete':
        cat_id = request.POST.get('category_id')
        Category.objects.filter(pk=cat_id).delete()
        messages.success(request, 'Category deleted')

    return render(request, 'wallpapers/admin_categories.html', {'categories': categories})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_tags(request):
    tag_counts = {}
    for wp in Wallpaper.objects.all().iterator():
        if wp.tags:
            if isinstance(wp.tags, list):
                for t in wp.tags:
                    tag_counts[t] = tag_counts.get(t, 0) + 1
            elif isinstance(wp.tags, str):
                for t in wp.tags.split(','):
                    t = t.strip().strip('[]" ').strip("'")
                    if t:
                        tag_counts[t] = tag_counts.get(t, 0) + 1
    sorted_tags = sorted(tag_counts.items(), key=lambda x: -x[1])
    max_count = sorted_tags[0][1] if sorted_tags else 1
    return render(request, 'wallpapers/admin_tags.html', {'tags': sorted_tags, 'max_count': max_count})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_toggle_ads(request):
    config, _ = SiteConfig.objects.get_or_create(key='ads_enabled', defaults={'value': 'false'})
    if config.value == 'true':
        config.value = 'false'
    else:
        config.value = 'true'
    config.save()
    status = 'enabled' if config.value == 'true' else 'disabled'
    messages.success(request, f'Google Ads {status}')
    return redirect('admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_users(request):
    days = int(request.GET.get('days', 30))
    since = datetime.now() - timedelta(days=days)

    top_downloaders = (
        Download.objects.filter(downloaded_at__gte=since)
        .values('user_id')
        .annotate(count=Count('id'))
        .order_by('-count')[:20]
    )

    daily_downloads = []
    for i in range(days):
        day = (datetime.now() - timedelta(days=days - 1 - i)).date()
        count = Download.objects.filter(downloaded_at__date=day).count()
        daily_downloads.append({'date': day.isoformat(), 'count': count})

    recent_downloads = Download.objects.select_related('wallpaper').order_by('-downloaded_at')[:30]

    return render(request, 'wallpapers/admin_users.html', {
        'top_downloaders': top_downloaders,
        'daily_downloads': daily_downloads,
        'recent_downloads': recent_downloads,
        'days': days,
    })


