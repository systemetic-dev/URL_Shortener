from celery import shared_task
from apps.shortener.models import URL
from django.utils import timezone

@shared_task
def record_click(url_id):

    url = URL.objects.get(id=url_id)

    url.click_count += 1
    url.save(update_fields=["click_count"])
    
@shared_task
def cleanup_expired_urls():

    expired_urls = URL.objects.filter(
        expires_at__lt=timezone.now(),
        is_active=True
    )

    count = expired_urls.update(is_active=False)

    return f"{count} expired URLs deactivated"