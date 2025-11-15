from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from .models import Subcontractor
from .forms import SubcontractorForm, SubcontractorFilterForm


@login_required
@permission_required('subcontractors.view_subcontractor', raise_exception=True)
def subcontractor_list(request):
    subcontractors = Subcontractor.objects.all()
    form = SubcontractorFilterForm(request.GET)

    if form.is_valid():
        contractor_type = form.cleaned_data.get('contractor_type')
        is_active = form.cleaned_data.get('is_active')
        search = form.cleaned_data.get('search')

        if contractor_type:
            subcontractors = subcontractors.filter(contractor_type=contractor_type)

        if is_active == 'true':
            subcontractors = subcontractors.filter(is_active=True)
        elif is_active == 'false':
            subcontractors = subcontractors.filter(is_active=False)

        if search:
            subcontractors = subcontractors.filter(
                Q(name__icontains=search) |
                Q(inn__icontains=search) |
                Q(director_name__icontains=search) |
                Q(email__icontains=search)
            )

    context = {
        'subcontractors': subcontractors,
        'filter_form': form,
    }
    return render(request, 'subcontractors/subcontractor_list.html', context)


@login_required
@permission_required('subcontractors.add_subcontractor', raise_exception=True)
def subcontractor_create(request):
    if request.method == 'POST':
        form = SubcontractorForm(request.POST)
        if form.is_valid():
            subcontractor = form.save()
            messages.success(request, f'Субподрядчик "{subcontractor.name}" успешно создан!')
            return redirect('subcontractors:list')
    else:
        form = SubcontractorForm()

    context = {'form': form}
    return render(request, 'subcontractors/subcontractor_form.html', context)


@login_required
@permission_required('subcontractors.change_subcontractor', raise_exception=True)
def subcontractor_edit(request, pk):
    subcontractor = get_object_or_404(Subcontractor, pk=pk)

    if request.method == 'POST':
        form = SubcontractorForm(request.POST, instance=subcontractor)
        if form.is_valid():
            subcontractor = form.save()
            messages.success(request, f'Субподрядчик "{subcontractor.name}" успешно обновлен!')
            return redirect('subcontractors:list')
    else:
        form = SubcontractorForm(instance=subcontractor)

    context = {'form': form, 'subcontractor': subcontractor}
    return render(request, 'subcontractors/subcontractor_form.html', context)


@login_required
@permission_required('subcontractors.delete_subcontractor', raise_exception=True)
def subcontractor_delete(request, pk):
    subcontractor = get_object_or_404(Subcontractor, pk=pk)

    if request.method == 'POST':
        name = subcontractor.name
        subcontractor.delete()
        messages.success(request, f'Субподрядчик "{name}" успешно удален!')
        return redirect('subcontractors:list')

    context = {'subcontractor': subcontractor}
    return render(request, 'subcontractors/subcontractor_confirm_delete.html', context)


@login_required
@permission_required('subcontractors.change_subcontractor', raise_exception=True)
def subcontractor_toggle_active(request, pk):
    subcontractor = get_object_or_404(Subcontractor, pk=pk)
    subcontractor.is_active = not subcontractor.is_active
    subcontractor.save()

    status = "активен" if subcontractor.is_active else "неактивен"
    messages.success(request, f'Субподрядчик "{subcontractor.name}" теперь {status}!')

    return redirect('subcontractors:list')

@login_required
@permission_required('subcontractors.view_subcontractor', raise_exception=True)
def subcontractor_detail(request, pk):
    subcontractor = get_object_or_404(Subcontractor, pk=pk)
    context = {'subcontractor': subcontractor}
    return render(request, 'subcontractors/subcontractor_detail.html', context)