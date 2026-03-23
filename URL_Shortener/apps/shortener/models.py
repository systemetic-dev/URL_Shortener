from django.db import models

# Create your models here.
from django.conf import settings
from .services import encode_base62


class URL(models.Model):
    original_url = models.URLField()

    short_code = models.CharField(
        max_length=10,
        unique=True,
        db_index=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    click_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.id:
            super().save(*args, **kwargs)

            self.short_code = encode_base62(self.id)

            super().save(update_fields=["short_code"])
            return

        super().save(*args, **kwargs)