from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Contractor, Service
from .forms import ContractorForm, ServiceForm


@login_required
def contractors_list(request):
    contractors = Contractor.objects.all()
    return render(request, 'contractors/contractors_list.html', {'contractors': contractors})


@login_required
def contractor_detail(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)
    services = contractor.services.all()

    if request.method == 'POST':
        service_form = ServiceForm(request.POST)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.contractor = contractor
            service.save()
            return redirect('contractors:contractor_detail', pk=contractor.pk)  # добавил пространство имен
    else:
        service_form = ServiceForm()

    return render(request, 'contractors/contractor_detail.html', {
        'contractor': contractor,
        'services': services,
        'service_form': service_form
    })


@login_required
def contractor_create(request):
    if request.method == 'POST':
        form = ContractorForm(request.POST)
        if form.is_valid():
            contractor = form.save()
            return redirect('contractors:contractors_list')  # добавил пространство имен
    else:
        form = ContractorForm()

    return render(request, 'contractors/contractor_form.html', {'form': form})


@login_required
def contractor_edit(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)

    if request.method == 'POST':
        form = ContractorForm(request.POST, instance=contractor)
        if form.is_valid():
            form.save()
            return redirect('contractors:contractors_list')  # добавил пространство имен
    else:
        form = ContractorForm(instance=contractor)

    return render(request, 'contractors/contractor_form.html', {'form': form})


@login_required
def contractor_delete(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)

    if request.method == 'POST':
        contractor.delete()
        return redirect('contractors:contractors_list')  # добавил пространство имен

    return render(request, 'contractors/contractor_confirm_delete.html', {'contractor': contractor})