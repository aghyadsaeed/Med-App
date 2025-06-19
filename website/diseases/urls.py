from django.urls import path
from . import views

urlpatterns = [
    path('', views.disease_list, name='disease_list'),
    path('disease/<int:pk>/', views.disease_detail, name='disease_detail'),
    path('disease/new/', views.disease_new, name='disease_new'),
    path('disease/<int:pk>/edit/', views.disease_edit, name='disease_edit'),
    path('disease/<int:pk>/delete/', views.delete_disease, name='delete_disease'),
    path('disease/<int:pk>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('download_all/', views.download_all_diseases, name='download_all_diseases'),
    path('add_folder/', views.add_folder, name='add_folder'),
    path('folders/<int:folder_id>/delete/', views.delete_folder, name='delete_folder'),

]
