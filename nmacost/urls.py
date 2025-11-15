from django.urls import path
from . import views

app_name = 'nmacost'

urlpatterns = [
    path('', views.nmacost_list, name='nmacost-list'),
    path('create/', views.nmacost_create, name='nmacost-create'),
    path('<int:nmacost_id>/', views.nmacost_detail, name='nmacost-detail'),
    path('<int:nmacost_id>/edit/', views.nmacost_edit, name='nmacost-edit'),
    path('<int:nmacost_id>/resource/add/', views.resource_add, name='resource-add'),
    path('<int:nmacost_id>/export/pdf/', views.export_pdf, name='export-pdf'),
    path('<int:nmacost_id>/export/excel/', views.export_excel, name='export-excel'),
    path('<int:nmacost_id>/export/word/', views.export_word, name='export-word'),
]