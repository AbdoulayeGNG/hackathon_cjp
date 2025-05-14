from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('create/', views.create_report, name='create'),
    path('detail/<int:pk>/', views.report_detail, name='detail'),
    path('list/', views.report_list, name='list'),
    path('update/<int:pk>/', views.update_report, name='update'),
]