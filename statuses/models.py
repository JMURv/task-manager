from django.db import models
from django.urls import reverse


class Status(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Status name'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created'
    )
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('status_list')
