from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name=_('Label name')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list_labels')
