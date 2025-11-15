from django.urls import path
from . import views

app_name = 'subcontractors'

urlpatterns = [
    path('', views.subcontractor_list, name='list'),
    path('create/', views.subcontractor_create, name='create'),
    path('<int:pk>/edit/', views.subcontractor_edit, name='edit'),
    path('<int:pk>/delete/', views.subcontractor_delete, name='delete'),
    path('<int:pk>/toggle-active/', views.subcontractor_toggle_active, name='toggle_active'),
    path('<int:pk>/', views.subcontractor_detail, name='detail'),  # Добавьте этот путь
]