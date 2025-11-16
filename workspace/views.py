from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Workspace, Project, WorkspaceMember
from .forms import ProjectForm, WorkspaceMemberForm


@login_required
def workspace_dashboard(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    # Проверка доступа пользователя к workspace
    if not WorkspaceMember.objects.filter(workspace=workspace, user=request.user).exists():
        messages.error(request, "У вас нет доступа к этой рабочей области")
        return redirect('login:home')

    projects = workspace.projects.all()
    members = workspace.members.all()

    context = {
        'workspace': workspace,
        'projects': projects,
        'members': members,
    }
    return render(request, 'workspace/dashboard.html', context)


@login_required
def project_create(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    if not WorkspaceMember.objects.filter(workspace=workspace, user=request.user, role__in=['owner', 'admin']).exists():
        messages.error(request, "У вас нет прав для создания проектов")
        return redirect('workspace:workspace_dashboard', workspace_id=workspace_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.workspace = workspace
            project.save()
            messages.success(request, "Проект успешно создан")
            return redirect('workspace:workspace_dashboard', workspace_id=workspace_id)
    else:
        form = ProjectForm()

    context = {
        'form': form,
        'workspace': workspace,
        'title': 'Создание проекта',
    }
    return render(request, 'workspace/project_form.html', context)


@login_required
def project_edit(request, workspace_id, project_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    project = get_object_or_404(Project, id=project_id, workspace=workspace)

    if not WorkspaceMember.objects.filter(workspace=workspace, user=request.user, role__in=['owner', 'admin']).exists():
        messages.error(request, "У вас нет прав для редактирования проектов")
        return redirect('workspace:workspace_dashboard', workspace_id=workspace_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Проект успешно обновлен")
            return redirect('workspace:workspace_dashboard', workspace_id=workspace_id)
    else:
        form = ProjectForm(instance=project)

    context = {
        'form': form,
        'workspace': workspace,
        'project': project,
        'title': 'Редактирование проекта',
    }
    return render(request, 'workspace/project_form.html', context)


@login_required
def project_delete(request, workspace_id, project_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    project = get_object_or_404(Project, id=project_id, workspace=workspace)

    if not WorkspaceMember.objects.filter(workspace=workspace, user=request.user, role__in=['owner', 'admin']).exists():
        messages.error(request, "У вас нет прав для удаления проектов")
        return redirect('workspace:workspace_dashboard', workspace_id=workspace_id)

    if request.method == 'POST':
        project.delete()
        messages.success(request, "Проект успешно удален")
        return redirect('workspace:workspace_dashboard', workspace_id=workspace_id)

    context = {
        'workspace': workspace,
        'project': project,
    }
    return render(request, 'workspace/project_confirm_delete.html', context)


@login_required
def project_detail(request, workspace_id, project_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    project = get_object_or_404(Project, id=project_id, workspace=workspace)

    if not WorkspaceMember.objects.filter(workspace=workspace, user=request.user).exists():
        messages.error(request, "У вас нет доступа к этому проекту")
        return redirect('workspace:workspace_dashboard', workspace_id=workspace_id)

    context = {
        'workspace': workspace,
        'project': project,
    }
    return render(request, 'workspace/project_detail.html', context)


@login_required
def manage_members(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    if not WorkspaceMember.objects.filter(workspace=workspace, user=request.user, role__in=['owner', 'admin']).exists():
        messages.error(request, "У вас нет прав для управления участниками")
        return redirect('workspace:workspace_dashboard', workspace_id=workspace_id)

    members = workspace.members.all()

    if request.method == 'POST':
        form = WorkspaceMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.workspace = workspace
            member.save()
            messages.success(request, "Участник успешно добавлен")
            return redirect('workspace:manage_members', workspace_id=workspace_id)
    else:
        form = WorkspaceMemberForm()

    context = {
        'workspace': workspace,
        'members': members,
        'form': form,
    }
    return render(request, 'workspace/manage_members.html', context)


@login_required
def remove_member(request, workspace_id, member_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    if not WorkspaceMember.objects.filter(workspace=workspace, user=request.user, role__in=['owner', 'admin']).exists():
        messages.error(request, "У вас нет прав для управления участниками")
        return redirect('workspace:workspace_dashboard', workspace_id=workspace_id)

    member = get_object_or_404(WorkspaceMember, id=member_id, workspace=workspace)

    if request.method == 'POST':
        member.delete()
        messages.success(request, "Участник успешно удален")

    return redirect('workspace:manage_members', workspace_id=workspace_id)