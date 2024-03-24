from django.urls import path
from . import views

urlpatterns = [
    #Home view for datareporting
    path('home', views.home_view, name='datareporting_home'),

    path('reports', views.reports_view, name='reports'),
    path('reports/new_report', views.new_report, name='new_report'),
    path('reports/new_report/add_report', views.add_report, name='add_report'),
    path('reports/report_datasets/<int:report_id>', views.report_datasets, name='report_datasets'),
    path('reports/report_datasets/<int:report_id>/amend_report', views.amend_report, name='amend_report'),
    path('reports/report_datasets/<int:report_id>/amend_report/delete_report', views.delete_report_page, name='delete_report_page'),
    path('reports/report_datasets/<int:report_id>/amend_report/delete_report/delete', views.confirm_delete_report, name='confirm_delete_report'),
    path('reports/report_datasets/<int:report_id>/amend_report/update_report', views.update_report, name='update_report'),
    path('reports/update_parameter_values', views.update_parameter_values, name='update_parameter_values'),
    path('reports/update_report_active_status/<int:report_id>', views.update_report_active_status, name='update_report_active_status'),
    path('reports/report_datasets/<int:report_id>/update_parameter_values', views.update_parameter_values, name='update_parameter_values'),    

    path('datasets', views.datasets_view, name='datasets'),
    path('datasets/queue_dataset/<int:dataset_id>', views.queue_dataset, name='queue_dataset'),
    path('datasets/processing', views.dataset_processing, name='dataset_processing'),
    path('datasets/run_data_pull', views.run_data_pull, name='run_data_pull'),
    path('datasets/new_dataset', views.new_dataset, name='new_dataset'),
    path('datasets/new_dataset/add_dataset', views.add_dataset, name='add_dataset'),
    path('datasets/dataset_details/<int:dataset_id>', views.dataset_details, name='dataset_details'),
    path('datasets/dataset_details/<int:dataset_id>/amend_dataset', views.amend_dataset, name='amend_dataset'),
    path('datasets/dataset_details/<int:dataset_id>/amend_dataset/update_dataset', views.update_dataset, name='update_dataset'),
    path('datasets/dataset_details/<int:dataset_id>/amend_dataset/delete_dataset', views.delete_dataset_page, name='delete_dataset_page'),
    path('datasets/dataset_details/<int:dataset_id>/amend_dataset/delete_dataset/delete', views.confirm_delete_dataset, name='confirm_delete_dataset'),
    
    
]
