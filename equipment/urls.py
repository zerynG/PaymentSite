from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('', views.EquipmentListView.as_view(), name='list'),
    path('create/', views.EquipmentCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.EquipmentUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.EquipmentDeleteView.as_view(), name='delete'),
    path('calculate/<int:equipment_id>/', views.calculate_service_cost, name='calculate'),
]