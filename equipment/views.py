from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Equipment
from .forms import EquipmentForm


class EquipmentListView(ListView):
    model = Equipment
    template_name = 'equipment/equipment_list.html'
    context_object_name = 'equipment_list'

    def get_queryset(self):
        return Equipment.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем счетчик активных инструментов в контекст
        context['active_equipment_count'] = Equipment.objects.filter(is_active=True).count()
        return context


class EquipmentCreateView(CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:list')

    def form_valid(self, form):
        messages.success(self.request, 'Оборудование успешно добавлено')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем счетчик активных инструментов в контекст
        context['active_equipment_count'] = Equipment.objects.filter(is_active=True).count()
        return context


class EquipmentUpdateView(UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:list')

    def form_valid(self, form):
        messages.success(self.request, 'Оборудование успешно обновлено')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем счетчик активных инструментов в контекст
        context['active_equipment_count'] = Equipment.objects.filter(is_active=True).count()
        return context


class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = 'equipment/equipment_confirm_delete.html'
    success_url = reverse_lazy('equipment:list')

    def delete(self, request, *args, **kwargs):
        equipment = self.get_object()
        equipment.is_active = False
        equipment.save()
        messages.success(request, 'Оборудование успешно удалено')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем счетчик активных инструментов в контекст
        context['active_equipment_count'] = Equipment.objects.filter(is_active=True).count()
        return context


def calculate_service_cost(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    quantity = request.GET.get('quantity', 0)
    try:
        quantity = float(quantity)
        cost = equipment.calculate_service_cost(quantity)
        return JsonResponse({'cost': float(cost)})
    except ValueError:
        return JsonResponse({'error': 'Неверное количество'}, status=400)


# Дополнительная функция для получения счетчика активных инструментов
def get_active_equipment_count(request):
    """API endpoint для получения количества активных инструментов"""
    count = Equipment.objects.filter(is_active=True).count()
    return JsonResponse({'active_equipment_count': count})


# Модельный метод для получения счетчика (опционально)
def get_active_equipment_count_model():
    """Функция для получения количества активных инструментов из модели"""
    return Equipment.objects.filter(is_active=True).count()