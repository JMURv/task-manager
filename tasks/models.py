from django.db import models
from statuses.models import Status
from labels.models import Label
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(
        verbose_name=_('Task name'),
        max_length=200,
        unique=True
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='creator',
        verbose_name=_('Author')
    )
    executor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=_('Executor'),
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        Label,
        through='TaskLabels',
        verbose_name=_('Label'),
        blank=True
    )

    def __str__(self):
        return self.name


class TaskLabels(models.Model):
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE)
    labels = models.ForeignKey(Label, on_delete=models.PROTECT)
