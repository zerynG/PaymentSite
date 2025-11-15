from django import forms
from .models import Project, ProjectResource
from customers.models import Customer
from employees.models import Employee
from contractors.models import Contractor
from subcontractors.models import Subcontractor
from equipment.models import Equipment


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 'start_date', 'end_date', 'description', 'customer',
            'technical_spec', 'tax_rate'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ProjectResourceForm(forms.ModelForm):
    class Meta:
        model = ProjectResource
        fields = [
            'name', 'resource_type', 'employee', 'contractor',
            'subcontractor', 'equipment', 'service_name',
            'start_date', 'end_date', 'quantity', 'margin'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Динамически скрываем ненужные поля в зависимости от типа ресурса
        self.fields['employee'].queryset = Employee.objects.all()
        self.fields['contractor'].queryset = Contractor.objects.all()
        self.fields['subcontractor'].queryset = Subcontractor.objects.all()
        self.fields['equipment'].queryset = Equipment.objects.all()