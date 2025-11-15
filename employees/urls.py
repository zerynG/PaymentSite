from django.urls import path
from . import views

app_name = 'employees'  # это создает пространство имен

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('create/', views.employee_create, name='employee_create'),  # ДОЛЖНО БЫТЬ
    path('edit/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('toggle-active/<int:pk>/', views.employee_toggle_active, name='employee_toggle_active'),
]