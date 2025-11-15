from django.urls import path
from . import views

app_name = 'workspace'

urlpatterns = [
    path('<int:workspace_id>/dashboard/', views.workspace_dashboard, name='workspace_dashboard'),
    path('<int:workspace_id>/project/create/', views.project_create, name='project_create'),
    path('<int:workspace_id>/project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:workspace_id>/project/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('<int:workspace_id>/project/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('<int:workspace_id>/members/', views.manage_members, name='manage_members'),
    path('<int:workspace_id>/members/<int:member_id>/remove/', views.remove_member, name='remove_member'),
]