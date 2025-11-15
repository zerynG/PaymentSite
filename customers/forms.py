from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['inn', 'customer_type', 'name', 'full_name', 'email', 'phone']
        widgets = {
            'inn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ИНН'
            }),
            'customer_type': forms.Select(attrs={
                'class': 'form-control',
                'onchange': 'toggleCompanyName()'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название',
                'id': 'company-name-field'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ФИО'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите телефон'
            }),
        }

    def clean_inn(self):
        inn = self.cleaned_data.get('inn')
        # Проверка на уникальность ИНН
        if Customer.objects.filter(inn=inn).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Заказчик с таким ИНН уже существует')
        return inn