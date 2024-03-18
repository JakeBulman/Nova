from django.urls import path
from . import views

urlpatterns = [
    #Home view for datareporting
    path('home', views.datareporting_home_view, name='datareporting_home'),
    path('reports', views.reports_view, name='reports'),
    path('reports/new_report', views.new_report, name='new_report'),
    path('reports/new_report/add_report', views.add_report, name='add_report'),
    path('reports/report_datasets/<int:id>', views.report_datasets, name='report_datasets'),
    path('update_parameter_values', views.update_parameter_values, name='update_parameter_values'),
    path('update_report_active_status/<int:report_id>', views.update_report_active_status, name='update_report_active_status'),
    path('datasets', views.datasets_view, name='datasets'),
    path('run_data_load/<int:dataset_id>', views.run_data_load_view, name='run_data_load'),
    path('update_active_status/<int:dataset_id>', views.dataset_update_status, name='update_active_status'),
    path('new_dataset', views.new_dataset, name='new_dataset'),
    path('new_dataset/add_dataset', views.add_dataset, name='add_dataset'),
]
