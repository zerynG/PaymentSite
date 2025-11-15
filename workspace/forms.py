from django import forms
from .models import Project, Workspace, WorkspaceMember
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Название проекта',
            'description': 'Описание',
            'status': 'Статус',
            'deadline': 'Срок выполнения',
        }


class WorkspaceMemberForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Пользователь",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = WorkspaceMember
        fields = ['user', 'role']
        labels = {
            'role': 'Роль',
        }