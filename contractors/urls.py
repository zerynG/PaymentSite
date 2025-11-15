from django.urls import path
from . import views

app_name = 'contractors'

urlpatterns = [
    path('', views.contractors_list, name='contractors_list'),
    path('new/', views.contractor_create, name='contractor_create'),
    path('<int:pk>/', views.contractor_detail, name='contractor_detail'),
    path('<int:pk>/edit/', views.contractor_edit, name='contractor_edit'),
    path('<int:pk>/delete/', views.contractor_delete, name='contractor_delete'),
]