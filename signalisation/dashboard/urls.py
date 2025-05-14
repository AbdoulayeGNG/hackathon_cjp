from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('administration/', views.dashboard, name='dashboard'),
    path('administration/report/<int:report_id>/update-status/', views.update_report_status, name='update_status'),
    path('admin-dashboard/', views.admin_dashboard, name='admin'),
    path('admin/manage/<int:report_id>/', views.manage_report, name='manage_report'),

#    Desktop\HACHATON\signalisation\dashboard\urls.py
path('admins/', views.admin_list, name='admin_list'),
path('admins/create/', views.admin_create, name='admin_create'),
path('admins/<int:admin_id>/edit/', views.admin_edit, name='admin_edit'),
path('admins/<int:admin_id>/delete/', views.admin_delete, name='admin_delete'),
]