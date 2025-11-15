from django import forms
from .models import Contractor, Service

class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = [
            'last_name', 'first_name', 'middle_name',
            'contract_type', 'tax_rate',
            'default_unit', 'default_rate'
        ]
        widgets = {
            'contract_type': forms.Select(choices=Contractor.CONTRACTOR_TYPE_CHOICES),
            'tax_rate': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
            'default_unit': forms.Select(choices=Contractor.UNIT_CHOICES),
            'default_rate': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'unit', 'rate']
        widgets = {
            'unit': forms.Select(choices=Service.UNIT_CHOICES),
            'rate': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }