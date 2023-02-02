from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Status name')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('status_list')
