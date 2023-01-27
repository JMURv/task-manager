from django.db import models
from statuses.models import Status
from labels.models import Label
from django.contrib.auth import get_user_model


class Task(models.Model):
    name = models.CharField(
        'Имя',
        max_length=200,
        unique=True
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='creator',
        verbose_name='Автор'
    )
    executor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name='Исполнитель',
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        Label, through='TaskLabels',
        verbose_name='Метки',
        blank=True
    )

    def __str__(self):
        return self.name


class TaskLabels(models.Model):
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE)
    labels = models.ForeignKey(Label, on_delete=models.PROTECT)
