from django.db import models
from django.contrib.auth.models import User


class NMACost(models.Model):
    # Временно закомментируем связь с Project
    # project = models.OneToOneField('projects.Project', on_delete=models.CASCADE, verbose_name="Проект", null=True, blank=True)

    # Временное поле для названия проекта
    project_name = models.CharField(max_length=200, verbose_name="Название проекта", default="Неизвестный проект")

    development_period = models.CharField(max_length=100, verbose_name="Срок разработки")
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Итоговая стоимость", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Стоимость НМА"
        verbose_name_plural = "Стоимости НМА"

    def __str__(self):
        return f"НМА: {self.project_name} - {self.total_cost} руб."


class ResourceItem(models.Model):
    nmacost = models.ForeignKey(NMACost, on_delete=models.CASCADE, related_name='resources')
    name = models.CharField(max_length=200, verbose_name="Наименование ресурса")
    description = models.TextField(verbose_name="Описание", blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")
    unit = models.CharField(max_length=50, verbose_name="Единица измерения")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость за единицу")
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Общая стоимость")

    class Meta:
        verbose_name = "Ресурс"
        verbose_name_plural = "Ресурсы"

    def __str__(self):
        return f"{self.name} - {self.total_cost} руб."

    def save(self, *args, **kwargs):
        # Автоматически рассчитываем общую стоимость
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)