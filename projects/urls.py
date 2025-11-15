from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:project_pk>/add-resource/', views.add_resource, name='add_resource'),
    path('resource/<int:resource_pk>/delete/', views.delete_resource, name='delete_resource'),
]