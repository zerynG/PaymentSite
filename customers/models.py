from django.db import models


class Customer(models.Model):
    CUSTOMER_TYPES = (
        ('individual', 'Физическое лицо'),
        ('entrepreneur', 'Индивидуальный предприниматель'),
        ('legal', 'Юридическое лицо'),
    )

    inn = models.CharField('ИНН', max_length=12, unique=True)
    customer_type = models.CharField(
        'Тип Заказчика',
        max_length=20,
        choices=CUSTOMER_TYPES
    )
    name = models.CharField(
        'Название',
        max_length=255,
        blank=True,
        null=True
    )
    full_name = models.CharField('ФИО', max_length=255)
    email = models.EmailField('Контактный e-mail')
    phone = models.CharField('Контактный номер телефона', max_length=20)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'
        ordering = ['-created_at']

    def __str__(self):
        if self.customer_type == 'individual':
            return f"ФЛ: {self.full_name} (ИНН: {self.inn})"
        elif self.customer_type == 'entrepreneur':
            return f"ИП: {self.name or self.full_name} (ИНН: {self.inn})"
        else:
            return f"ЮЛ: {self.name} (ИНН: {self.inn})"

    def save(self, *args, **kwargs):
        # Очищаем название для физических лиц
        if self.customer_type == 'individual':
            self.name = None
        super().save(*args, **kwargs)