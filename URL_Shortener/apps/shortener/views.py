from django.core.cache import cache
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from apps.analytics.tasks import record_click
from .models import URL


def redirect_url(request, short_code):

    cache_key = f"url:{short_code}"

    original_url = cache.get(cache_key)

    if not original_url:

        url = get_object_or_404(URL, short_code=short_code)

        if not url.is_active:
            return redirect("/")

        if url.expires_at and url.expires_at < timezone.now():
            return redirect("/")

        original_url = url.original_url

        # Store in Redis for future requests
        cache.set(cache_key, original_url, timeout=3600)
        # Record the click asynchronously        
        record_click.delay(url.id)

    return redirect(original_url)