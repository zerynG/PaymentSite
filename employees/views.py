from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .models import Employee
from .forms import EmployeeForm, EmployeeFilterForm


def employee_list(request):
    """Список сотрудников с фильтрацией"""
    employees = Employee.objects.all()
    filter_form = EmployeeFilterForm(request.GET or None)

    if filter_form.is_valid():
        position = filter_form.cleaned_data.get('position')
        active_only = filter_form.cleaned_data.get('active_only')

        if position:
            employees = employees.filter(position__icontains=position)
        if active_only:
            employees = employees.filter(is_active=True)

    context = {
        'employees': employees,
        'filter_form': filter_form,
    }
    return render(request, 'employees/employee_list.html', context)


def employee_create(request):
    """Создание нового сотрудника"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Сотрудник {employee.get_full_name()} успешно добавлен!')
            return redirect('employees:employee_list')
    else:
        form = EmployeeForm()

    context = {'form': form, 'title': 'Добавить сотрудника'}
    return render(request, 'employees/employee_form.html', context)


def employee_edit(request, pk):
    """Редактирование сотрудника"""
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Данные сотрудника {employee.get_full_name()} обновлены!')
            return redirect('employees:employee_list')
    else:
        form = EmployeeForm(instance=employee)

    context = {'form': form, 'title': 'Редактировать сотрудника', 'employee': employee}
    return render(request, 'employees/employee_form.html', context)


def employee_delete(request, pk):
    """Удаление сотрудника"""
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee_name = employee.get_full_name()
        employee.delete()
        messages.success(request, f'Сотрудник {employee_name} удален!')
        return redirect('employees:employee_list')

    context = {'employee': employee}
    return render(request, 'employees/employee_confirm_delete.html', context)


def employee_toggle_active(request, pk):
    """Активация/деактивация сотрудника"""
    if request.method != 'POST':
        messages.error(request, 'Неверный метод запроса')
        return redirect('employees:employee_list')
    
    employee = get_object_or_404(Employee, pk=pk)
    employee.is_active = not employee.is_active
    employee.save()

    action = "активирован" if employee.is_active else "деактивирован"
    messages.success(request, f'Сотрудник {employee.get_full_name()} {action}!')

    return redirect('employees:employee_list')


def calculate_employee_cost(request):
    """Расчет стоимости работы сотрудника (API endpoint)"""
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        working_days = request.POST.get('working_days')

        try:
            employee = Employee.objects.get(pk=employee_id, is_active=True)
            working_days = int(working_days)

            # Упрощенный расчет
            daily_cost = employee.calculate_daily_rate(working_days)
            total_cost = daily_cost * working_days

            return JsonResponse({
                'success': True,
                'daily_cost': round(daily_cost, 2),
                'total_cost': round(total_cost, 2),
                'employee_name': employee.get_full_name()
            })

        except (Employee.DoesNotExist, ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid parameters'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})