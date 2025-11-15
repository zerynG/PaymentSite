from django.urls import path
from . import views

app_name = 'commercial_proposal'

urlpatterns = [
    path('', views.proposal_list, name='proposal_list'),  # корневой путь /commercial/
    path('create/', views.create_proposal, name='create_proposal'),
    path('<int:pk>/', views.proposal_detail, name='proposal_detail'),
    path('<int:pk>/pdf/', views.download_pdf, name='download_pdf'),
    path('<int:pk>/excel/', views.download_excel, name='download_excel'),
    path('<int:pk>/word/', views.download_word, name='download_word'),
    path('debug/', views.debug_urls, name='debug_urls'),
]