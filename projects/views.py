from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone  # ← Добавьте этот импорт

from .models import Project, ProjectResource
from .forms import ProjectForm, ProjectResourceForm

@login_required
def project_list(request):
    projects = Project.objects.filter(created_by=request.user)
    context = {
        'projects': projects,
        'today': timezone.now().date()  # Теперь timezone определен
    }
    return render(request, 'projects/project_list.html', context)

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Проект успешно создан!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, created_by=request.user)
    resources = project.projectresource_set.all()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            project.calculate_costs()
            messages.success(request, 'Проект успешно обновлен!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'form': form,
        'resources': resources
    })


@login_required
def add_resource(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, created_by=request.user)

    if request.method == 'POST':
        form = ProjectResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.project = project
            resource.calculate_costs()
            resource.save()
            project.calculate_costs()
            messages.success(request, 'Ресурс успешно добавлен!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectResourceForm()

    return render(request, 'projects/add_resource.html', {
        'project': project,
        'form': form
    })


@login_required
def delete_resource(request, resource_pk):
    resource = get_object_or_404(ProjectResource, pk=resource_pk)
    project = resource.project

    if project.created_by != request.user:
        messages.error(request, 'У вас нет прав для удаления этого ресурса!')
        return redirect('project_detail', pk=project.pk)

    resource.delete()
    project.calculate_costs()
    messages.success(request, 'Ресурс успешно удален!')
    return redirect('project_detail', pk=project.pk)