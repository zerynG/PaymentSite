from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from io import BytesIO

# Проверка доступности библиотек
try:
    from xhtml2pdf import pisa
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping

    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    import pandas as pd

    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    from docx import Document

    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

from .models import NMACost, ResourceItem
from .forms import NMACostForm, ResourceItemForm


@login_required
def nmacost_list(request):
    """Список всех записей НМА"""
    nmacosts = NMACost.objects.all().prefetch_related('resources')

    # Статистика
    total_resources = ResourceItem.objects.count()
    total_cost_result = NMACost.objects.aggregate(total=Sum('total_cost'))
    total_cost = total_cost_result['total'] or 0

    # Пагинация
    paginator = Paginator(nmacosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'nmacost/nmacost_list.html', {
        'page_obj': page_obj,
        'total_resources': total_resources,
        'total_cost': total_cost,
        'has_pdf': HAS_PDF,
        'has_pandas': HAS_PANDAS,
        'has_docx': HAS_DOCX
    })


@login_required
def nmacost_detail(request, nmacost_id):
    """Детальная страница конкретной записи НМА"""
    nmacost = get_object_or_404(NMACost, id=nmacost_id)
    resources = nmacost.resources.all()

    return render(request, 'nmacost/nmacost_detail.html', {
        'nmacost': nmacost,
        'resources': resources,
        'has_pdf': HAS_PDF,
        'has_pandas': HAS_PANDAS,
        'has_docx': HAS_DOCX
    })


@login_required
def nmacost_create(request):
    """Создание новой записи НМА"""
    if request.method == 'POST':
        form = NMACostForm(request.POST)
        if form.is_valid():
            nmacost = form.save(commit=False)
            nmacost.total_cost = 0  # Начальная стоимость
            nmacost.save()
            return redirect('nmacost:nmacost-detail', nmacost_id=nmacost.id)
    else:
        form = NMACostForm()

    return render(request, 'nmacost/nmacost_form.html', {
        'form': form,
        'title': 'Создание стоимости НМА'
    })


@login_required
def nmacost_edit(request, nmacost_id):
    """Редактирование записи НМА"""
    nmacost = get_object_or_404(NMACost, id=nmacost_id)

    if request.method == 'POST':
        form = NMACostForm(request.POST, instance=nmacost)
        if form.is_valid():
            form.save()
            return redirect('nmacost:nmacost-detail', nmacost_id=nmacost.id)
    else:
        form = NMACostForm(instance=nmacost)

    return render(request, 'nmacost/nmacost_form.html', {
        'form': form,
        'title': 'Редактирование стоимости НМА',
        'nmacost': nmacost
    })


@login_required
def resource_add(request, nmacost_id):
    """Добавление ресурса к записи НМА"""
    nmacost = get_object_or_404(NMACost, id=nmacost_id)

    if request.method == 'POST':
        form = ResourceItemForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.nmacost = nmacost
            resource.save()  # total_cost рассчитывается автоматически в save() модели

            # Пересчитываем общую стоимость НМА
            total = sum(res.total_cost for res in nmacost.resources.all())
            nmacost.total_cost = total
            nmacost.save()

            return redirect('nmacost:nmacost-detail', nmacost_id=nmacost.id)
    else:
        form = ResourceItemForm()

    return render(request, 'nmacost/resource_form.html', {
        'form': form,
        'nmacost': nmacost
    })


@login_required
def export_pdf(request, nmacost_id):
    """Экспорт в PDF"""
    if not HAS_PDF:
        return HttpResponse("PDF export is not available. Please install xhtml2pdf.")

    nmacost = get_object_or_404(NMACost, id=nmacost_id)
    resources = nmacost.resources.all()

    html_string = render_to_string('nmacost/export_pdf.html', {
        'nmacost': nmacost,
        'resources': resources
    })

    result = BytesIO()
    
    # Используем правильную кодировку для кириллицы
    # xhtml2pdf требует строку в UTF-8, не BytesIO
    # Передаем строку напрямую, а не в BytesIO
    pdf = pisa.pisaDocument(
        html_string,
        result
    )

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="nmacost_{nmacost.id}.pdf"'
        return response

    return HttpResponse(f'Ошибка при создании PDF: {pdf.err}')


@login_required
def export_excel(request, nmacost_id):
    """Экспорт в Excel"""
    if not HAS_PANDAS:
        return HttpResponse("Excel export is not available. Please install pandas and openpyxl.")

    nmacost = get_object_or_404(NMACost, id=nmacost_id)
    resources = nmacost.resources.all()

    # Создаем простой CSV если нет pandas
    import csv
    from django.utils.encoding import smart_str

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="nmacost_{nmacost.id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Наименование', 'Описание', 'Количество', 'Единица', 'Цена за единицу', 'Общая стоимость'])

    for resource in resources:
        writer.writerow([
            smart_str(resource.name),
            smart_str(resource.description),
            resource.quantity,
            smart_str(resource.unit),
            resource.unit_cost,
            resource.total_cost
        ])

    return response


@login_required
def export_word(request, nmacost_id):
    """Экспорт в Word"""
    nmacost = get_object_or_404(NMACost, id=nmacost_id)
    resources = nmacost.resources.all()

    # Создаем простой текстовый файл
    content = f"Стоимость НМА: {nmacost.project_name}\n"
    content += f"Срок разработки: {nmacost.development_period}\n"
    content += f"Итоговая стоимость: {nmacost.total_cost} руб.\n\n"
    content += "Ресурсы:\n"

    for resource in resources:
        content += f"- {resource.name}: {resource.quantity} {resource.unit} × {resource.unit_cost} руб. = {resource.total_cost} руб.\n"
        if resource.description:
            content += f"  Описание: {resource.description}\n"

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="nmacost_{nmacost.id}.txt"'
    return response


@login_required
def nmacost_delete(request, nmacost_id):
    """Удаление записи НМА"""
    nmacost = get_object_or_404(NMACost, id=nmacost_id)

    if request.method == 'POST':
        project_name = nmacost.project_name
        nmacost.delete()
        messages.success(request, f'Стоимость НМА "{project_name}" успешно удалена!')
        return redirect('nmacost:nmacost-list')

    return render(request, 'nmacost/nmacost_confirm_delete.html', {
        'nmacost': nmacost
    })


@login_required
def resource_delete(request, nmacost_id, resource_id):
    """Удаление ресурса из записи НМА"""
    nmacost = get_object_or_404(NMACost, id=nmacost_id)
    resource = get_object_or_404(ResourceItem, id=resource_id, nmacost=nmacost)

    if request.method == 'POST':
        resource.delete()
        # Пересчитываем общую стоимость НМА
        total = sum(res.total_cost for res in nmacost.resources.all())
        nmacost.total_cost = total
        nmacost.save()
        messages.success(request, 'Ресурс успешно удален!')
        return redirect('nmacost:nmacost-detail', nmacost_id=nmacost.id)

    return render(request, 'nmacost/resource_confirm_delete.html', {
        'nmacost': nmacost,
        'resource': resource
    })