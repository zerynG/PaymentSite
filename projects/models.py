from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Project(models.Model):
    RESOURCE_TYPES = [
        ('employee', 'Сотрудник'),
        ('contractor', 'Исполнитель'),
        ('subcontractor', 'Субподрядчик'),
        ('equipment', 'Оборудование'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название проекта")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    description = models.TextField(verbose_name="Описание проекта", blank=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name="Заказчик")
    technical_spec = models.FileField(upload_to='technical_specs/',
                                      null=True, blank=True, verbose_name="Техническое задание")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20.00,
                                   verbose_name="Налоговая ставка (%)",
                                   validators=[MinValueValidator(0)])

    # Автоматически рассчитываемые поля
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     verbose_name="Итоговая стоимость")
    cost_price = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     verbose_name="Себестоимость")
    cost_with_margin = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                           verbose_name="Стоимость с маржинальностью")
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     verbose_name="Чистая прибыль")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def calculate_costs(self):
        resources = self.projectresource_set.all()

        # Расчет себестоимости
        self.cost_price = sum(resource.cost_price for resource in resources)

        # Расчет стоимости с маржей
        self.cost_with_margin = sum(resource.final_cost for resource in resources)

        # Расчет чистой прибыли
        self.net_profit = sum(resource.final_cost - resource.cost_price for resource in resources)

        # Расчет итоговой стоимости с налогом
        tax_multiplier = 1 + (self.tax_rate / 100)
        self.total_cost = self.cost_with_margin * tax_multiplier

        self.save()

    def __str__(self):
        return self.name


class ProjectResource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('contractor', 'Исполнитель'),
        ('subcontractor', 'Субподрядчик'),
        ('equipment', 'Оборудование'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Название ресурса")
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES,
                                     verbose_name="Тип ресурса")

    # Ссылки на различные типы ресурсов
    employee = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    contractor = models.ForeignKey('contractors.Contractor', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    subcontractor = models.ForeignKey('subcontractors.Subcontractor', on_delete=models.SET_NULL,
                                      null=True, blank=True)
    equipment = models.ForeignKey('equipment.Equipment', on_delete=models.SET_NULL,
                                  null=True, blank=True)

    service_name = models.CharField(max_length=200, verbose_name="Название услуги")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1,
                                   verbose_name="Количество")
    margin = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                 verbose_name="Маржинальность (%)",
                                 validators=[MinValueValidator(0)])

    # Автоматически рассчитываемые поля
    cost_price = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     verbose_name="Себестоимость")
    final_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     verbose_name="Итоговая стоимость")

    def calculate_costs(self):
        # Расчет в зависимости от типа ресурса
        if self.resource_type == 'employee' and self.employee:
            base_cost = self.employee.hourly_rate * self.quantity
        elif self.resource_type == 'contractor' and self.contractor:
            base_cost = self.contractor.hourly_rate * self.quantity
        elif self.resource_type == 'subcontractor' and self.subcontractor:
            base_cost = self.subcontractor.daily_rate * self.quantity
        elif self.resource_type == 'equipment' and self.equipment:
            base_cost = self.equipment.rental_cost * self.quantity
        else:
            base_cost = 0

        self.cost_price = base_cost
        margin_multiplier = 1 + (self.margin / 100)
        self.final_cost = base_cost * margin_multiplier
        self.save()

    def __str__(self):
        return f"{self.name} - {self.project.name}"